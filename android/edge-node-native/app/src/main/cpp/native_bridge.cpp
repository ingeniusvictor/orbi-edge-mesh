#include <jni.h>

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <mutex>
#include <sstream>
#include <string>
#include <vector>

#include "llama.h"

namespace {

std::mutex g_mutex;
llama_model* g_model = nullptr;
int g_context_size = 4096;
int g_threads = 4;
std::string g_last_metrics_json =
    "{\"status\":\"not_run\"}";

void set_metrics_error(const char* code) {
    std::ostringstream json;
    json << "{"
         << "\"status\":\"error\","
         << "\"code\":\"" << code << "\""
         << "}";
    g_last_metrics_json = json.str();
}

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
        set_metrics_error("MODEL_NOT_LOADED");
        return env->NewStringUTF("ERROR: MODEL_NOT_LOADED");
    }

    if (prompt_value == nullptr) {
        set_metrics_error("PROMPT_NULL");
        return env->NewStringUTF("ERROR: PROMPT_NULL");
    }

    const char* prompt_chars = env->GetStringUTFChars(prompt_value, nullptr);
    if (prompt_chars == nullptr) {
        set_metrics_error("PROMPT_UTF8");
        return env->NewStringUTF("ERROR: PROMPT_UTF8");
    }

    const std::string prompt(prompt_chars);
    env->ReleaseStringUTFChars(prompt_value, prompt_chars);

    const llama_vocab* vocab = llama_model_get_vocab(g_model);
    if (vocab == nullptr) {
        set_metrics_error("VOCAB_UNAVAILABLE");
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
        set_metrics_error("TOKEN_COUNT_UNEXPECTED");
        return env->NewStringUTF("ERROR: TOKEN_COUNT_UNEXPECTED");
    }

    const int n_prompt = -token_count_result;
    if (n_prompt <= 0) {
        set_metrics_error("EMPTY_TOKENIZATION");
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
        set_metrics_error("TOKENIZATION_FAILED");
        return env->NewStringUTF("ERROR: TOKENIZATION_FAILED");
    }

    const int max_possible = g_context_size - n_prompt - 1;
    const int max_tokens = std::min(
        std::max(1, static_cast<int>(requested_max_tokens)),
        max_possible
    );

    if (max_tokens <= 0) {
        set_metrics_error("CONTEXT_TOO_SMALL");
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
        set_metrics_error("CONTEXT_CREATE_FAILED");
        return env->NewStringUTF("ERROR: CONTEXT_CREATE_FAILED");
    }

    llama_sampler_chain_params sampler_params = llama_sampler_chain_default_params();
    sampler_params.no_perf = false;

    llama_sampler* sampler = llama_sampler_chain_init(sampler_params);
    if (sampler == nullptr) {
        set_metrics_error("SAMPLER_CREATE_FAILED");
        llama_free(ctx);
        return env->NewStringUTF("ERROR: SAMPLER_CREATE_FAILED");
    }

    llama_sampler_chain_add(sampler, llama_sampler_init_greedy());

    llama_batch batch = llama_batch_get_one(
        prompt_tokens.data(),
        static_cast<int32_t>(prompt_tokens.size())
    );

    std::string output;
    using Clock = std::chrono::steady_clock;
    const auto total_start = Clock::now();
    double prompt_decode_ms = 0.0;
    double generation_phase_ms = 0.0;
    int generated_tokens = 0;
    bool first_decode = true;

    for (int generated = 0; generated < max_tokens; ++generated) {
        const auto decode_start = Clock::now();
        if (llama_decode(ctx, batch) != 0) {
            set_metrics_error("DECODE_FAILED");
            llama_sampler_free(sampler);
            llama_free(ctx);
            return env->NewStringUTF("ERROR: DECODE_FAILED");
        }
        const auto decode_end = Clock::now();
        const double decode_ms =
            std::chrono::duration<double, std::milli>(
                decode_end - decode_start
            ).count();

        if (first_decode) {
            prompt_decode_ms = decode_ms;
            first_decode = false;
        } else {
            generation_phase_ms += decode_ms;
        }

        llama_token token = llama_sampler_sample(sampler, ctx, -1);

        if (llama_vocab_is_eog(vocab, token)) {
            break;
        }

        output += token_piece(vocab, token);
        generated_tokens += 1;
        batch = llama_batch_get_one(&token, 1);
    }

    const auto total_end = Clock::now();
    const double total_ms =
        std::chrono::duration<double, std::milli>(
            total_end - total_start
        ).count();

    const double prompt_tps =
        prompt_decode_ms > 0.0
            ? static_cast<double>(n_prompt) / (prompt_decode_ms / 1000.0)
            : 0.0;

    const int timed_generation_tokens =
        std::max(0, generated_tokens - 1);

    const double generation_tps =
        generation_phase_ms > 0.0 && timed_generation_tokens > 0
            ? static_cast<double>(timed_generation_tokens) /
                (generation_phase_ms / 1000.0)
            : 0.0;

    std::ostringstream metrics;
    metrics << std::fixed << std::setprecision(3)
            << "{"
            << "\"status\":\"ok\","
            << "\"prompt_tokens\":" << n_prompt << ","
            << "\"generated_tokens\":" << generated_tokens << ","
            << "\"prompt_decode_ms\":" << prompt_decode_ms << ","
            << "\"generation_decode_ms\":" << generation_phase_ms << ","
            << "\"total_generation_loop_ms\":" << total_ms << ","
            << "\"prompt_tokens_per_second\":" << prompt_tps << ","
            << "\"generation_tokens_per_second\":" << generation_tps << ","
            << "\"context_size\":" << g_context_size << ","
            << "\"threads\":" << g_threads
            << "}";
    g_last_metrics_json = metrics.str();

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
    return env->NewStringUTF(g_last_metrics_json.c_str());
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
