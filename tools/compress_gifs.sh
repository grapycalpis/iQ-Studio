#!/bin/bash
# Copyright (c) 2025 Innodisk Corp.
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# compress_gifs.sh - Scan GIFs and recommend gifski compression for files >= 20 MB.
#
# Default behavior (no --apply) is read-only: scan and report.
# With --apply, the tool compresses qualifying files in place with gifski --quality 70.
# It auto-detects source fps and refuses to overwrite when the compressed result is
# not smaller than the original.

set -euo pipefail

THRESHOLD_BYTES=$((20 * 1024 * 1024))
QUALITY=70
APPLY=false
PATHS=()

usage() {
    cat <<'EOF'
Usage: tools/compress_gifs.sh [--apply] [PATH ...]

Scan GIF files and recommend compression for those >= 20 MB.

Options:
  --apply       Compress qualifying GIFs in place with gifski --quality 70.
                Without this flag, the tool only reports.
  -h, --help    Show this help.

Examples:
  tools/compress_gifs.sh                            # scan from current dir
  tools/compress_gifs.sh tutorials/                 # scan one subtree
  tools/compress_gifs.sh --apply path/to/x.gif      # compress one file
  tools/compress_gifs.sh --apply tutorials/sdks/    # compress a subtree

Requirements for --apply: ffmpeg and gifski must be in PATH.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --apply) APPLY=true; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; while [[ $# -gt 0 ]]; do PATHS+=("$1"); shift; done; break ;;
        -*) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
        *) PATHS+=("$1"); shift ;;
    esac
done

[[ ${#PATHS[@]} -eq 0 ]] && PATHS=(".")

if [[ "$APPLY" == "true" ]]; then
    for cmd in ffmpeg ffprobe gifski; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            echo "ERROR: '$cmd' not found in PATH." >&2
            echo "Install with one of:" >&2
            echo "  sudo apt install ffmpeg" >&2
            echo "  brew install ffmpeg gifski   (linuxbrew, no sudo)" >&2
            exit 1
        fi
    done
fi

mapfile -t GIFS < <(find "${PATHS[@]}" -type f \( -iname '*.gif' \) ! -path '*/.git/*' 2>/dev/null | sort)

if [[ ${#GIFS[@]} -eq 0 ]]; then
    echo "No GIF files found under: ${PATHS[*]}"
    exit 0
fi

LARGE=0
DONE=0
SKIPPED=0

for gif in "${GIFS[@]}"; do
    size=$(stat -c%s "$gif")
    if (( size < THRESHOLD_BYTES )); then
        continue
    fi
    LARGE=$((LARGE + 1))

    if [[ "$APPLY" == "false" ]]; then
        printf "[LARGE] %s  (%s)\n" "$gif" "$(numfmt --to=iec "$size")"
        continue
    fi

    echo "Compressing: $gif ($(numfmt --to=iec "$size"))"

    fps_raw=$(ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate \
              -of default=nw=1:nk=1 "$gif")
    fps=$(awk -F'/' '{ if ($2==0) print 15; else printf "%.0f", $1/$2 }' <<< "$fps_raw")
    (( fps < 5 )) && fps=15

    tmpdir=$(mktemp -d)
    ffmpeg -loglevel error -y -i "$gif" -vsync vfr "$tmpdir/f_%04d.png"

    out="$tmpdir/out.gif"
    if ! gifski --quiet --output "$out" --quality "$QUALITY" --fps "$fps" "$tmpdir"/f_*.png; then
        echo "  ERROR: gifski failed"
        rm -rf "$tmpdir"
        continue
    fi

    new=$(stat -c%s "$out")
    if (( new >= size )); then
        printf "  Skipped: compressed (%s) >= original (%s)\n" \
            "$(numfmt --to=iec "$new")" "$(numfmt --to=iec "$size")"
        SKIPPED=$((SKIPPED + 1))
        rm -rf "$tmpdir"
        continue
    fi

    mv "$out" "$gif"
    ratio=$(awk "BEGIN{ printf \"%.1fx\", $size/$new }")
    printf "  Done: %s -> %s (%s smaller)\n" \
        "$(numfmt --to=iec "$size")" "$(numfmt --to=iec "$new")" "$ratio"
    DONE=$((DONE + 1))

    rm -rf "$tmpdir"
done

echo ""
if [[ "$APPLY" == "false" ]]; then
    if (( LARGE == 0 )); then
        echo "All GIFs are under $(numfmt --to=iec $THRESHOLD_BYTES). No action needed."
    else
        echo "Found $LARGE GIF(s) >= $(numfmt --to=iec $THRESHOLD_BYTES)."
        echo ""
        echo "Recommended: compress with gifski --quality $QUALITY."
        echo "Run:"
        echo "  bash tools/compress_gifs.sh --apply ${PATHS[*]}"
    fi
else
    echo "Summary: $DONE compressed, $SKIPPED skipped."
fi
