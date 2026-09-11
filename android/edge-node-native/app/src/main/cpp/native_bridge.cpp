#include <jni.h>

extern "C"
JNIEXPORT jstring JNICALL
Java_com_orbi_edgenode_NativeBridge_nativeStatus(
    JNIEnv* env,
    jobject /* thiz */
) {
    return env->NewStringUTF("JNI BRIDGE READY");
}
