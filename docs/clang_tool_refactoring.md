# Clang Tool Refactoring

[TOC]

## Caveats

*   The current workflow requires git.
*   This doesn't work on Windows... yet. I'm hoping to have a proof-of-concept
    working on Windows as well ~~in a month~~ several centuries from now.

## Prerequisites

Everything needed should be in a default Chromium checkout using gclient.
`third_party/llvm-build/Release+Asserts/bin` should be in your `$PATH`.

## Writing the Tool

An example clang tool is being implemented in
https://codereview.chromium.org/12746010/. Other useful resources might be the
[basic tutorial for Clang's AST matchers](http://clang.llvm.org/docs/LibASTMatchersTutorial.html)
or the
[AST matcher reference](http://clang.llvm.org/docs/LibASTMatchersReference.html).

Build your tool by running the following command (requires cmake version 2.8.10
or later):

```shell
tools/clang/scripts/update.py --force-local-build --without-android \
--tools <tools>
```

`<tools>` is a semicolon delimited list of subdirectories in `tools/clang` to
build. The resulting binary will end up in
`third_party/llvm-build/Release+Asserts/bin`. For example, to build the Chrome
plugin and the empty\_string tool, run the following:

```shell
tools/clang/scripts/update.py --force-local-build --without-android \
--tools plugins empty_string
```

When writing AST matchers, the following can be helpful to see what clang thinks
the AST is:

```shell
clang++ -cc1 -ast-dump foo.cc
```

## Running the tool

First, you'll need to generate the compilation database with the following
command:

```shell
cd $HOME/src/chrome/src
ninja -C out/Debug -t compdb cc cxx objc objcxx > \
out/Debug/compile_commands.json
```

This will dump the command lines used to build the C/C++ modules in all of
Chromium into the resulting file. Then run the following command to run your
tool across all Chromium code:

```shell
# Make sure all chromium targets are built to avoid missing generated
# dependencies
ninja -C out/Debug
tools/clang/scripts/run_tool.py <toolname> \
<path/to/directory/with/compile_commands.json> <path 1> <path 2> ...
```

`<path 1>`, `<path 2>`, etc are optional arguments you use to filter the files
that will be rewritten. For example, if you only want to run the `empty-string`
tool on files in `chrome/browser/extensions` and `sync`, you'd do something like:

```shell
tools/clang/scripts/run_tool.py empty_string out/Debug \
chrome/browser/extensions sync
```

## Limitations

Since the compile database is generated by ninja, that means that files that
aren't compiled on that platform won't be processed. That means if you want to
apply a change across all Chromium platforms, you'll have to run the tool once
on each platform.

## Testing

`test_tool.py` is the test harness for running tests. To use it, simply run:

```shell
test_tool.py <tool name>
```

Note that name of the built tool and the subdirectory it lives in at
`tools/clang` must match. What the test harness does is find all files that
match the pattern `*-original.cc` in your tool's tests subdirectory. It then
runs the tool across those files and compares it to the expected result, stored
in `*-expected.cc`
