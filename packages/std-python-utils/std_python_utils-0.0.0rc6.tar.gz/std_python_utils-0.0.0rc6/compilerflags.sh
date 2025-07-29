
CANDCPPFLAGS='-Wall -Werror -Wextra -fpic -flto -mtune=cortex-a76'

CONLYFLAGS='-std=c23'
CPPONLYFLAGS='-std=c++23'
GCCCONLYFLAGS='-fanalyzer -fconcepts -fmodules-ts'
CFLAGS=$CONLYFLAGS

CXXFLAGS=$CPPONLYFLAGS
CPPFLAGS=$CANDCPPFLAGS