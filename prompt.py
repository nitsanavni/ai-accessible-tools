import openai
from filecache import filecache

from verify import semi, verify


@filecache(1e9)
def prompt(the_prompt: str, sample=0) -> str:
    return (
        openai.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": the_prompt}]
        )
        .choices[0]
        .message.content
    )


def test_prompt():
    """
    Thought:
    The user is initiating a classic "knock knock" joke. The typical response is to continue the joke by saying "Who's there?"

    Answer:
    Who's there?
    """
    a_prompt = """format: format your response as described in the <format> section, but don't include the <format> tags.
<format>
Thought:
{think first, you thoughts here}
Answer:
{your answer here}
</format>
<query>
knock knock
</query>"""
    verify(prompt(a_prompt), options=semi)
