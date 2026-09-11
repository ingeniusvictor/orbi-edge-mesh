#include <jni.h>

#include "llama.h"

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
