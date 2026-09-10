import unittest

from workloads.classifier import classify_workload
from workloads.profiles import get_profile


class WorkloadClassifierTests(unittest.TestCase):
    def test_short_llm(self):
        self.assertEqual(
            classify_workload(service_type="llm", requested_output_tokens=128),
            "chat_short",
        )

    def test_long_llm(self):
        self.assertEqual(
            classify_workload(service_type="llm", requested_output_tokens=1024),
            "generation_long",
        )

    def test_embedding(self):
        self.assertEqual(
            classify_workload(service_type="embedding"),
            "embedding",
        )

    def test_profile_lookup(self):
        profile = get_profile("text_to_speech")
        self.assertEqual(profile.service_type, "text_to_speech")
        self.assertEqual(profile.latency_sensitivity, "high")


if __name__ == "__main__":
    unittest.main()
