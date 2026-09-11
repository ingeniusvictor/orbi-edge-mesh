#include <jni.h>

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <mutex>
#include <string>
#include <vector>

#include "llama.h"

namespace {

std::mutex g_mutex;
llama_model* g_model = nullptr;
int g_context_size = 4096;
int g_threads = 4;
int g_last_generated_tokens = 0;
double g_last_generation_ms = 0.0;

jstring utf8_to_jstring(JNIEnv* env, const std::string& value) {
    std::vector<jchar> utf16;
    utf16.reserve(value.size());

    const auto replacement = [&utf16]() {
        utf16.push_back(static_cast<jchar>(0xFFFD));
    };

    for (size_t i = 0; i < value.size();) {
        const unsigned char lead = static_cast<unsigned char>(value[i]);
        uint32_t codepoint = 0;
        size_t length = 0;
        uint32_t minimum = 0;

        if (lead <= 0x7F) {
            codepoint = lead;
            length = 1;
            minimum = 0;
        } else if ((lead & 0xE0) == 0xC0) {
            codepoint = lead & 0x1F;
            length = 2;
            minimum = 0x80;
        } else if ((lead & 0xF0) == 0xE0) {
            codepoint = lead & 0x0F;
            length = 3;
            minimum = 0x800;
        } else if ((lead & 0xF8) == 0xF0) {
            codepoint = lead & 0x07;
            length = 4;
            minimum = 0x10000;
        } else {
            replacement();
            ++i;
            continue;
        }

        if (i + length > value.size()) {
            replacement();
            break;
        }

        bool valid = true;
        for (size_t offset = 1; offset < length; ++offset) {
            const unsigned char continuation =
                static_cast<unsigned char>(value[i + offset]);
            if ((continuation & 0xC0) != 0x80) {
                valid = false;
                break;
            }
            codepoint = (codepoint << 6) | (continuation & 0x3F);
        }

        if (
            !valid ||
            codepoint < minimum ||
            codepoint > 0x10FFFF ||
            (codepoint >= 0xD800 && codepoint <= 0xDFFF)
        ) {
            replacement();
            ++i;
            continue;
        }

        if (codepoint <= 0xFFFF) {
            utf16.push_back(static_cast<jchar>(codepoint));
        } else {
            codepoint -= 0x10000;
            utf16.push_back(
                static_cast<jchar>(0xD800 + ((codepoint >> 10) & 0x3FF))
            );
            utf16.push_back(
                static_cast<jchar>(0xDC00 + (codepoint & 0x3FF))
            );
        }

        i += length;
    }

    return env->NewString(
        utf16.empty() ? nullptr : utf16.data(),
        static_cast<jsize>(utf16.size())
    );
}

std::string token_piece(const llama_vocab* vocab, llama_token token) {
    char small[256];
    int n = llama_token_to_piece(vocab, token, small, sizeof(small), 0, true);

    if (n >= 0) {
        return std::string(small, static_cast<size_t>(n));
    }

    const int required = -n;
    std::vector<char> large(static_cast<size_t>(required));
    n = llama_token_to_piece(vocab, token, large.data(), large.size(), 0, true);

    if (n < 0) {
        return {};
    }

    return std::string(large.data(), static_cast<size_t>(n));
}

bool format_single_user_chat(
    const llama_model* model,
    const std::string& user_text,
    std::string* formatted
) {
    if (formatted == nullptr) {
        return false;
    }

    const char* tmpl = llama_model_chat_template(model, nullptr);
    if (tmpl == nullptr) {
        *formatted = user_text;
        return true;
    }

    llama_chat_message message{
        "user",
        user_text.c_str(),
    };

    std::vector<char> buffer(
        std::max<size_t>(512, user_text.size() * 3 + 256)
    );

    int written = llama_chat_apply_template(
        tmpl,
        &message,
        1,
        true,
        buffer.data(),
        static_cast<int32_t>(buffer.size())
    );

    if (written < 0) {
        return false;
    }

    if (written > static_cast<int>(buffer.size())) {
        buffer.resize(static_cast<size_t>(written));
        written = llama_chat_apply_template(
            tmpl,
            &message,
            1,
            true,
            buffer.data(),
            static_cast<int32_t>(buffer.size())
        );
    }

    if (written < 0 || written > static_cast<int>(buffer.size())) {
        return false;
    }

    formatted->assign(buffer.data(), static_cast<size_t>(written));
    return true;
}

void unload_locked() {
    if (g_model != nullptr) {
        llama_model_free(g_model);
        g_model = nullptr;
    }
}

}  // namespace

extern "C"
JNIEXPORT jstring JNICALL
Java_com_orbi_edgenode_NativeBridge_nativeStatus(
    JNIEnv* env,
    jobject /* thiz */
) {
    return env->NewStringUTF("JNI BRIDGE READY");
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_orbi_edgenode_NativeBridge_llamaSystemInfoNative(
    JNIEnv* env,
    jobject /* thiz */
) {
    const char* info = llama_print_system_info();
    if (info == nullptr) {
        return env->NewStringUTF("LLAMA LINKED; SYSTEM INFO UNAVAILABLE");
    }
    return env->NewStringUTF(info);
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_orbi_edgenode_NativeBridge_loadModelNative(
    JNIEnv* env,
    jobject /* thiz */,
    jstring model_path,
    jint context_size,
    jint threads
) {
    std::lock_guard<std::mutex> lock(g_mutex);

    if (model_path == nullptr) {
        return env->NewStringUTF("ERROR: MODEL_PATH_NULL");
    }

    const char* path_chars = env->GetStringUTFChars(model_path, nullptr);
    if (path_chars == nullptr) {
        return env->NewStringUTF("ERROR: MODEL_PATH_UTF8");
    }

    const std::string path(path_chars);
    env->ReleaseStringUTFChars(model_path, path_chars);

    unload_locked();

    ggml_backend_load_all();

    llama_model_params params = llama_model_default_params();
    params.n_gpu_layers = 0;

    g_model = llama_model_load_from_file(path.c_str(), params);
    if (g_model == nullptr) {
        return env->NewStringUTF("ERROR: MODEL_LOAD_FAILED");
    }

    g_context_size = std::max(512, static_cast<int>(context_size));
    g_threads = std::max(1, static_cast<int>(threads));

    return env->NewStringUTF("MODEL LOADED");
}

extern "C"
JNIEXPORT jboolean JNICALL
Java_com_orbi_edgenode_NativeBridge_isModelLoadedNative(
    JNIEnv* /* env */,
    jobject /* thiz */
) {
    std::lock_guard<std::mutex> lock(g_mutex);
    return g_model != nullptr ? JNI_TRUE : JNI_FALSE;
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_orbi_edgenode_NativeBridge_generateNative(
    JNIEnv* env,
    jobject /* thiz */,
    jstring prompt_value,
    jint requested_max_tokens
) {
    std::lock_guard<std::mutex> lock(g_mutex);

    if (g_model == nullptr) {
        return env->NewStringUTF("ERROR: MODEL_NOT_LOADED");
    }

    if (prompt_value == nullptr) {
        return env->NewStringUTF("ERROR: PROMPT_NULL");
    }

    const char* prompt_chars = env->GetStringUTFChars(prompt_value, nullptr);
    if (prompt_chars == nullptr) {
        return env->NewStringUTF("ERROR: PROMPT_UTF8");
    }

    const std::string user_prompt(prompt_chars);
    env->ReleaseStringUTFChars(prompt_value, prompt_chars);

    std::string prompt;
    if (!format_single_user_chat(g_model, user_prompt, &prompt)) {
        return env->NewStringUTF("ERROR: CHAT_TEMPLATE_FAILED");
    }

    const llama_vocab* vocab = llama_model_get_vocab(g_model);
    if (vocab == nullptr) {
        return env->NewStringUTF("ERROR: VOCAB_UNAVAILABLE");
    }

    const int token_count_result = llama_tokenize(
        vocab,
        prompt.c_str(),
        static_cast<int32_t>(prompt.size()),
        nullptr,
        0,
        true,
        true
    );

    if (token_count_result >= 0) {
        return env->NewStringUTF("ERROR: TOKEN_COUNT_UNEXPECTED");
    }

    const int n_prompt = -token_count_result;
    if (n_prompt <= 0) {
        return env->NewStringUTF("ERROR: EMPTY_TOKENIZATION");
    }

    std::vector<llama_token> prompt_tokens(static_cast<size_t>(n_prompt));
    const int tokenized = llama_tokenize(
        vocab,
        prompt.c_str(),
        static_cast<int32_t>(prompt.size()),
        prompt_tokens.data(),
        static_cast<int32_t>(prompt_tokens.size()),
        true,
        true
    );

    if (tokenized < 0) {
        return env->NewStringUTF("ERROR: TOKENIZATION_FAILED");
    }

    const int max_possible = g_context_size - n_prompt - 1;
    const int max_tokens = std::min(
        std::max(1, static_cast<int>(requested_max_tokens)),
        max_possible
    );

    if (max_tokens <= 0) {
        return env->NewStringUTF("ERROR: CONTEXT_TOO_SMALL");
    }

    llama_context_params ctx_params = llama_context_default_params();
    ctx_params.n_ctx = static_cast<uint32_t>(g_context_size);
    ctx_params.n_batch = static_cast<uint32_t>(
        std::max(32, std::min(g_context_size, n_prompt))
    );
    ctx_params.n_threads = g_threads;
    ctx_params.n_threads_batch = g_threads;
    ctx_params.no_perf = false;

    llama_context* ctx = llama_init_from_model(g_model, ctx_params);
    if (ctx == nullptr) {
        return env->NewStringUTF("ERROR: CONTEXT_CREATE_FAILED");
    }

    llama_sampler_chain_params sampler_params = llama_sampler_chain_default_params();
    sampler_params.no_perf = false;

    llama_sampler* sampler = llama_sampler_chain_init(sampler_params);
    if (sampler == nullptr) {
        llama_free(ctx);
        return env->NewStringUTF("ERROR: SAMPLER_CREATE_FAILED");
    }

    llama_sampler_chain_add(sampler, llama_sampler_init_greedy());

    llama_batch batch = llama_batch_get_one(
        prompt_tokens.data(),
        static_cast<int32_t>(prompt_tokens.size())
    );

    std::string output;
    g_last_generated_tokens = 0;
    g_last_generation_ms = 0.0;
    const auto generation_start = std::chrono::steady_clock::now();

    for (int generated = 0; generated < max_tokens; ++generated) {
        if (llama_decode(ctx, batch) != 0) {
            llama_sampler_free(sampler);
            llama_free(ctx);
            return env->NewStringUTF("ERROR: DECODE_FAILED");
        }

        llama_token token = llama_sampler_sample(sampler, ctx, -1);

        if (llama_vocab_is_eog(vocab, token)) {
            break;
        }

        output += token_piece(vocab, token);
        batch = llama_batch_get_one(&token, 1);
        g_last_generated_tokens += 1;
    }

    const auto generation_end = std::chrono::steady_clock::now();
    g_last_generation_ms = std::chrono::duration<double, std::milli>(
        generation_end - generation_start
    ).count();

    llama_sampler_free(sampler);
    llama_free(ctx);

    return utf8_to_jstring(env, output);
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_orbi_edgenode_NativeBridge_lastGenerationMetricsNative(
    JNIEnv* env,
    jobject /* thiz */
) {
    std::lock_guard<std::mutex> lock(g_mutex);

    const double seconds = g_last_generation_ms / 1000.0;
    const double tps = seconds > 0.0
        ? static_cast<double>(g_last_generated_tokens) / seconds
        : 0.0;

    std::ostringstream out;
    out << std::fixed << std::setprecision(3)
        << "tokens=" << g_last_generated_tokens
        << "; inference_wall_ms=" << g_last_generation_ms
        << "; output_tokens_per_second_wall=" << tps;

    return env->NewStringUTF(out.str().c_str());
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_orbi_edgenode_NativeBridge_unloadModelNative(
    JNIEnv* env,
    jobject /* thiz */
) {
    std::lock_guard<std::mutex> lock(g_mutex);
    unload_locked();
    return env->NewStringUTF("MODEL UNLOADED");
}
