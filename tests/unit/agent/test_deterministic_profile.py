from windows_use.llms.google import ChatGoogle


def test_google_llm_default_is_deterministic():
    llm = ChatGoogle(model="test-model")
    assert hasattr(llm, 'temperature')
    assert llm.temperature == 0.0
    assert hasattr(llm, 'profile')
