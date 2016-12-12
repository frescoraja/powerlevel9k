# vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8
################################################################
# Utility functions
# This file holds some utility-functions for
# the powerlevel9k-ZSH-theme
# https://github.com/bhilburn/powerlevel9k
################################################################

# Exits with 0 if a variable has been previously defined (even if empty)
# Takes the name of a variable that should be checked.
function defined() {
  local varname="$1"

  typeset -p "$varname" > /dev/null 2>&1
}

# Given the name of a variable and a default value, sets the variable
# value to the default only if it has not been defined.
#
# Typeset cannot set the value for an array, so this will only work
# for scalar values.
function set_default() {
  local varname="$1"
  local default_value="$2"

  defined "$varname" || typeset -g "$varname"="$default_value"
}

# Converts large memory values into a human-readable unit (e.g., bytes --> GB)
# Takes two arguments:
#   * $size - The number which should be prettified
#   * $base - The base of the number (default Bytes)
printSizeHumanReadable() {
  typeset -F 2 size
  size="$1"+0.00001
  local extension
  extension=('B' 'K' 'M' 'G' 'T' 'P' 'E' 'Z' 'Y')
  local index=1

  # if the base is not Bytes
  if [[ -n $2 ]]; then
    for idx in "${extension[@]}"; do
      if [[ "$2" == "$idx" ]]; then
        break
      fi
      index=$(( index + 1 ))
    done
  fi

  while (( (size / 1024) > 0.1 )); do
    size=$(( size / 1024 ))
    index=$(( index + 1 ))
  done

  echo "$size${extension[$index]}"
}

# Gets the first value out of a list of items that is not empty.
# The items are examined by a callback-function.
# Takes two arguments:
#   * $list - A list of items
#   * $callback - A callback function to examine if the item is
#                 worthy. The callback function has access to
#                 the inner variable $item.
function getRelevantItem() {
  local -a list
  local callback
  # Explicitly split the elements by whitespace.
  list=(${=1})
  callback=$2

  for item in $list; do
    # The first non-empty item wins
    try=$(eval "$callback")
    if [[ -n "$try" ]]; then
      echo "$try"
      break;
    fi
  done
}

# OS detection for the `os_icon` segment
case $(uname) in
    Darwin)
      OS='OSX'
      ;;
    FreeBSD)
      OS='BSD'
      ;;
    OpenBSD)
      OS='BSD'
      ;;
    DragonFly)
      OS='BSD'
      ;;
    Linux)
      OS='Linux'
      ;;
    SunOS)
      OS='Solaris'
      ;;
    *)
      OS=''
      OS_ICON=''
      ;;
esac

# Determine the correct sed parameter.
#
# `sed` is unfortunately not consistent across OSes when it comes to flags.
SED_EXTENDED_REGEX_PARAMETER="-r"
if [[ "$OS" == 'OSX' ]]; then
  local IS_BSD_SED="$(sed --version &>> /dev/null || echo "BSD sed")"
  if [[ -n "$IS_BSD_SED" ]]; then
    SED_EXTENDED_REGEX_PARAMETER="-E"
  fi
fi

# Determine if the passed segment is used in the prompt
#
# Pass the name of the segment to this function to test for its presence in
# either the LEFT or RIGHT prompt arrays.
#    * $1: The segment to be tested.
segment_in_use() {
    local key=$1
    if [[ -n "${POWERLEVEL9K_LEFT_PROMPT_ELEMENTS[(r)$key]}" ]] || [[ -n "${POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS[(r)$key]}" ]]; then
        return 0
    else
        return 1
    fi
}

# Search for a segment in a list of segments.
# Ignores the "_joined" suffix of segments.
#   * $1: The segment to be searched for
#   * $2: The array of segments to be searched in
get_indices_of_segment() {
  local segment="${1}"
  local -a list
  # Explicitly split the elements by whitespace.
  list=(${=2})

  local indices=()
  for ((i=1;$#list[i];i++)); do
    # Segments could be joined, but that is not an issue here.
    # So we strip the "_joined" indicator away.
    local currentSegment="${list[i]%_joined}"
    if [[ "${currentSegment}" == "${segment}" ]]; then
      indices+=("${i}")
    fi
  done

  echo "${indices[@]}"
}

# Print a deprecation warning if an old segment is in use.
# Takes the name of an associative array that contains the
# deprecated segments as keys, the values contain the new
# segment names.
print_deprecation_warning() {
  typeset -AH raw_deprecated_segments
  raw_deprecated_segments=(${(kvP@)1})

  for key in ${(@k)raw_deprecated_segments}; do
    if segment_in_use $key; then
      # segment is deprecated
      print -P "%F{yellow}Warning!%f The '$key' segment is deprecated. Use '%F{blue}${raw_deprecated_segments[$key]}%f' instead. For more informations, have a look at the CHANGELOG.md."
    fi
  done
}

# Given a directory path, truncate it according to the settings for
# `truncate_from_right`
function truncatePathFromRight() {
  local delim_len=${#POWERLEVEL9K_SHORTEN_DELIMITER}
  echo $1 | sed $SED_EXTENDED_REGEX_PARAMETER \
 "s@(([^/]{$((POWERLEVEL9K_SHORTEN_DIR_LENGTH))})([^/]{$delim_len}))[^/]+/@\2$POWERLEVEL9K_SHORTEN_DELIMITER/@g"
}
