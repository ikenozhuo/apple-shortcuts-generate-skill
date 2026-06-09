#!/bin/bash

set -e

AGENTS_DIR="$HOME/.agents/skills"
CLAUDE_DIR="$HOME/.claude/skills"

mkdir -p "$AGENTS_DIR"
mkdir -p "$CLAUDE_DIR"

CURRENT_DIR="$(pwd)"

find_skill_dirs() {
  local dirs=()

  if [ -f "$CURRENT_DIR/SKILL.md" ]; then
    dirs+=("$CURRENT_DIR")
  else
    while IFS= read -r dir; do
      dirs+=("$dir")
    done < <(
      find "$CURRENT_DIR" \
        -mindepth 2 \
        -maxdepth 2 \
        -type f \
        -name "SKILL.md" \
        -exec dirname {} \; | sort
    )
  fi

  printf '%s\n' "${dirs[@]}"
}

link_skill() {
  local skill_dir="$1"
  local target_dir="$2"

  local skill_name
  skill_name="$(basename "$skill_dir")"

  local link_path="$target_dir/$skill_name"

  if [ -L "$link_path" ]; then
    local old_target
    old_target="$(readlink "$link_path")"

    if [ "$old_target" = "$skill_dir" ]; then
      echo "已存在，跳过：$link_path -> $skill_dir"
      return
    fi

    echo "已存在旧软链接，先移除：$link_path -> $old_target"
    rm "$link_path"
  elif [ -e "$link_path" ]; then
    echo "跳过：$link_path 已存在且不是软链接"
    return
  fi

  ln -s "$skill_dir" "$link_path"
  echo "创建成功：$link_path -> $skill_dir"
}

SKILL_DIRS=()
while IFS= read -r dir; do
  [ -n "$dir" ] && SKILL_DIRS+=("$dir")
done < <(find_skill_dirs)

if [ ${#SKILL_DIRS[@]} -eq 0 ]; then
  echo "不是有效的 skill 目录，也没有在当前文件夹下找到包含 SKILL.md 的 skill 文件夹。"
  exit 1
fi

echo "检测到以下 skill 目录："
echo ""

for dir in "${SKILL_DIRS[@]}"; do
  echo "- $dir"
done

echo ""
echo "请选择要链接到哪里："
echo "1) ~/.agents/skills"
echo "2) ~/.claude/skills"
echo "3) 两个都链接"
echo ""

read -p "请输入选项 [1/2/3]: " choice

echo ""

case "$choice" in
  1)
    for dir in "${SKILL_DIRS[@]}"; do
      link_skill "$dir" "$AGENTS_DIR"
    done
    ;;
  2)
    for dir in "${SKILL_DIRS[@]}"; do
      link_skill "$dir" "$CLAUDE_DIR"
    done
    ;;
  3)
    for dir in "${SKILL_DIRS[@]}"; do
      link_skill "$dir" "$AGENTS_DIR"
      link_skill "$dir" "$CLAUDE_DIR"
    done
    ;;
  *)
    echo "无效选项，已退出。"
    exit 1
    ;;
esac

echo ""
echo "执行完成。"