#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  # Initialize icon overrides
  _powerlevel9kInitializeIconOverrides

  # Precompile the Segment Separators here!
  _POWERLEVEL9K_LEFT_SEGMENT_SEPARATOR="$(print_icon 'LEFT_SEGMENT_SEPARATOR')"
  _POWERLEVEL9K_LEFT_SUBSEGMENT_SEPARATOR="$(print_icon 'LEFT_SUBSEGMENT_SEPARATOR')"
  _POWERLEVEL9K_LEFT_SEGMENT_END_SEPARATOR="$(print_icon 'LEFT_SEGMENT_END_SEPARATOR')"
  _POWERLEVEL9K_RIGHT_SEGMENT_SEPARATOR="$(print_icon 'RIGHT_SEGMENT_SEPARATOR')"
  _POWERLEVEL9K_RIGHT_SUBSEGMENT_SEPARATOR="$(print_icon 'RIGHT_SUBSEGMENT_SEPARATOR')"

  # Disable TRAP, so that we have more control how the segment is build,
  # as shUnit does not work with async commands.
  trap WINCH
}

function testColorOverridingForCleanStateWorks() {
  POWERLEVEL9K_VCS_CLEAN_FOREGROUND='cyan'
  POWERLEVEL9K_VCS_CLEAN_BACKGROUND='white'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  git init 1>/dev/null

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{white} %F{cyan} master %k%F{white}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test
  unset POWERLEVEL9K_VCS_CLEAN_FOREGROUND
  unset POWERLEVEL9K_VCS_CLEAN_BACKGROUND
}

function testColorOverridingForModifiedStateWorks() {
  POWERLEVEL9K_VCS_MODIFIED_FOREGROUND='red'
  POWERLEVEL9K_VCS_MODIFIED_BACKGROUND='yellow'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  git init 1>/dev/null
  git config user.email "test@powerlevel9k.theme"
  git config user.name  "Testing Tester"
  touch testfile
  git add testfile
  git commit -m "test" 1>/dev/null
  echo "test" > testfile

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{yellow} %F{red} master ● %k%F{yellow}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test

  unset POWERLEVEL9K_VCS_MODIFIED_FOREGROUND
  unset POWERLEVEL9K_VCS_MODIFIED_BACKGROUND
}

function testColorOverridingForUntrackedStateWorks() {
  POWERLEVEL9K_VCS_UNTRACKED_FOREGROUND='cyan'
  POWERLEVEL9K_VCS_UNTRACKED_BACKGROUND='yellow'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  git init 1>/dev/null
  touch testfile

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{yellow} %F{cyan} master ? %k%F{yellow}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test

  unset POWERLEVEL9K_VCS_UNTRACKED_FOREGROUND
  unset POWERLEVEL9K_VCS_UNTRACKED_BACKGROUND
}

function testGitIconWorks() {
  POWERLEVEL9K_VCS_GIT_ICON='Git-Icon'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  git init

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{green} %F{black%}Git-Icon%f %F{black} master %k%F{green}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test

  unset POWERLEVEL9K_VCS_GIT_ICON
}

function testGitlabIconWorks() {
  POWERLEVEL9K_VCS_GIT_GITLAB_ICON='GL-Icon'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  # Initialize an empty git repository and add a GitLab project as
  # remote origin. This is sufficient to show the GitLab-specific icon.
  git init
  git remote add origin https://gitlab.com/dritter/gitlab-test-project.git

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{green} %F{black%}GL-Icon%f %F{black} master %k%F{green}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test

  unset POWERLEVEL9K_VCS_GIT_GITLAB_ICON
}

function testBitbucketIconWorks() {
  POWERLEVEL9K_VCS_GIT_BITBUCKET_ICON='BB-Icon'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  # Initialize an empty git repository and add a BitBucket project as
  # remote origin. This is sufficient to show the BitBucket-specific icon.
  git init
  git remote add origin https://dritter@bitbucket.org/dritter/dr-test.git

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{green} %F{black%}BB-Icon%f %F{black} master %k%F{green}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test

  unset POWERLEVEL9K_VCS_GIT_BITBUCKET_ICON
}

function testGitHubIconWorks() {
  POWERLEVEL9K_VCS_GIT_GITHUB_ICON='GH-Icon'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  # Initialize an empty git repository and add a GitHub project as
  # remote origin. This is sufficient to show the GitHub-specific icon.
  git init
  git remote add origin https://github.com/dritter/test.git

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{green} %F{black%}GH-Icon%f %F{black} master %k%F{green}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test

  unset POWERLEVEL9K_VCS_GIT_GITHUB_ICON
}


function testMercurialIconWorks() {
  POWERLEVEL9K_VCS_HG_ICON='HG-Icon'

  FOLDER=/tmp/powerlevel9k-test/vcs-test
  mkdir -p $FOLDER
  cd $FOLDER
  hg init

  prompt_vcs "left" "1" "false"
  p9k_build_prompt_from_cache

  assertEquals "%K{green} %F{black%}HG-Icon%f %F{black} default %k%F{green}%f " "${PROMPT}"

  cd -
  rm -fr /tmp/powerlevel9k-test

  unset POWERLEVEL9K_VCS_HG_ICON
}

source shunit2/source/2.1/src/shunit2
