# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
{
  'targets': [
    {
      'target_name': 'system_webview_shell_apk',
      'type': 'none',
      'variables': {
        'apk_name': 'SystemWebViewShell',
        'java_in_dir': 'tools/WebViewShell',
        'resource_dir': 'tools/WebViewShell/res',
        'android_manifest_path': 'tools/WebViewShell/AndroidManifest.xml', # for lint
      },
      'includes': [
        '../build/java_apk.gypi',
      ],
    },
    {
      # android_webview_apk creates a .jar as a side effect. Any java
      # targets that need that .jar in their classpath should depend on this
      # target. For more details see the content_shell_apk_java target.
      'target_name': 'system_webview_shell_apk_java',
      'type': 'none',
      'dependencies': [
        'system_webview_shell_apk',
      ],
      'includes': [ '../build/apk_fake_jar.gypi' ],
    },
    {
      'target_name': 'system_webview_shell_page_cycler_apk',
      'type': 'none',
      'dependencies': [
        '../base/base.gyp:base_java_test_support',
        '../content/content_shell_and_tests.gyp:content_java_test_support',
        '../testing/android/on_device_instrumentation.gyp:broker_java',
        '../testing/android/on_device_instrumentation.gyp:require_driver_apk',
        'system_webview_shell_apk_java',
      ],
      'variables': {
        'apk_name': 'SystemWebViewShellPageCycler',
        'java_in_dir': '../android_webview/tools/PageCycler',
        'is_test_apk': 1,
        'test_type': 'instrumentation',
        'android_manifest_path': '../android_webview/tools/PageCycler/AndroidManifest.xml',
      },
      'includes': [
        '../build/java_apk.gypi',
        '../build/android/test_runner.gypi',
      ],
    },
    {
      'target_name': 'system_webview_shell_layout_test_apk',
      'type': 'none',
      'dependencies': [
        '../base/base.gyp:base_java_test_support',
        '../testing/android/on_device_instrumentation.gyp:broker_java',
        '../testing/android/on_device_instrumentation.gyp:require_driver_apk',
        'system_webview_shell_apk_java',
      ],
      'variables': {
        'apk_name': 'SystemWebViewShellLayoutTest',
        'java_in_dir': '../android_webview/tools/WebViewShellTest',
        'is_test_apk': 1,
        'test_type': 'instrumentation',
        'isolate_file': 'system_webview_shell_test_apk.isolate',
        'android_manifest_path': '../android_webview/tools/WebViewShellTest/AndroidManifest.xml',
      },
      'includes': [
        '../build/java_apk.gypi',
        '../build/android/test_runner.gypi',
      ]
    },
  ],
}
