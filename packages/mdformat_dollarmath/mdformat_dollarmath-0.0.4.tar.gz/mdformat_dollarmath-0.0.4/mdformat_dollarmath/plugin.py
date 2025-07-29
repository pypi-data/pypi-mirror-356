import os
import re
from typing import Mapping

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.dollarmath import dollarmath_plugin

softbreak_token = Token(type="softbreak", tag="", nesting=0, markup="\n")


def dollar_math_inline_double_to_block(md: MarkdownIt):
    def extract_math_inline_double(state: StateCore):
        i = 0
        while i < len(state.tokens):
            if state.tokens[i].type == "inline":
                inner_tokens = state.tokens[i].children
                j = 0
                while j < len(inner_tokens):
                    if inner_tokens[j].type == "math_inline_double":
                        level = state.tokens[i].level
                        state.tokens[i - 1].hidden = state.tokens[i + 1].hidden = False

                        if inner_tokens[j - 1].type in ["softbreak", "hardbreak"]:
                            inner_tokens.pop(j - 1)
                            j -= 1
                        if inner_tokens[j - 1].type == "text":
                            inner_tokens[j - 1].content = inner_tokens[
                                j - 1
                            ].content.rstrip()
                        if j < len(inner_tokens) - 1 and inner_tokens[j + 1].type in [
                            "softbreak",
                            "hardbreak",
                        ]:
                            inner_tokens.pop(j + 1)
                        if (
                            j < len(inner_tokens) - 1
                            and inner_tokens[j + 1].type == "text"
                        ):
                            inner_tokens[j + 1].content = inner_tokens[
                                j + 1
                            ].content.lstrip()
                        if len(inner_tokens) != j + 1:
                            state.tokens.insert(
                                i + 1,
                                Token(
                                    "inline",
                                    "",
                                    nesting=0,
                                    attrs={},
                                    children=inner_tokens[j + 1 :],
                                    level=level,
                                ),
                            )
                            state.tokens.insert(
                                i + 1,
                                Token(
                                    "paragraph_open",
                                    "p",
                                    nesting=1,
                                    attrs={},
                                    block=True,
                                ),
                            )
                        state.tokens.insert(
                            i + 1 if len(inner_tokens) != j + 1 else i + 2,
                            Token(
                                "math_block",
                                tag="math",
                                markup="$$",
                                nesting=0,
                                attrs={},
                                content=inner_tokens[j].content,
                                block=True,
                                level=level,
                            ),
                        )
                        if len(inner_tokens) != j + 1:
                            state.tokens.insert(
                                i + 1,
                                Token(
                                    "paragraph_close",
                                    "p",
                                    nesting=-1,
                                    attrs={},
                                    block=True,
                                ),
                            )
                        state.tokens[i].children = inner_tokens[:j]

                    j += 1
            i += 1

    md.core.ruler.after("inline", "math_inline_double_fix", extract_math_inline_double)


def update_mdit(mdit: MarkdownIt) -> None:
    mdit.use(
        dollarmath_plugin, double_inline=True, allow_blank_lines=True, allow_space=True
    )
    mdit.use(dollar_math_inline_double_to_block)


def format_math_block_content(content):
    # strip and remove blank lines
    content = re.sub(r"\n+", "\n", content.strip(), flags=re.DOTALL)
    if os.environ.get("MDFORMAT_DOLLARMATH_USE_ALIGNED", False):
        # for engines that do not support aligned in math mode
        content = re.sub(r"\\(begin|end){align\*?}", r"\\\1{aligned}", content)

    # remove additional white spaces in the end of the line
    content = re.sub(r"\s+$", "", content)

    return f"\n{content}\n"


def _math_inline_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"${node.content}$"


def _math_block_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${format_math_block_content(node.content)}$$"


def _math_block_label_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${format_math_block_content(node.content)}$$ ({node.info})"


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "math_inline": _math_inline_renderer,
    "math_block_label": _math_block_label_renderer,
    "math_block": _math_block_renderer,
}
