import openai
from filecache import filecache

from verify import semi, verify


@filecache
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
    This is the beginning of a knock-knock joke, and the usual response is to say "Who's there?"

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
