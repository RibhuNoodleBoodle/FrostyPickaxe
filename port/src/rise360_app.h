// rise360 - ReXGlue Recompiled Project
//
// Customize your app by overriding virtual hooks from rex::ReXApp.

#pragma once

#include <rex/rex_app.h>
#include <filesystem>

class Rise360App : public rex::ReXApp {
 public:
  using rex::ReXApp::ReXApp;

  static std::unique_ptr<rex::ui::WindowedApp> Create(
      rex::ui::WindowedAppContext& ctx) {
    return std::unique_ptr<Rise360App>(new Rise360App(ctx, "rise360",
        PPCImageConfig));
  }

  static void CleanStaleShm() {
    std::error_code ec;
    if (std::filesystem::exists("/dev/shm", ec)) {
      for (const auto& entry : std::filesystem::directory_iterator("/dev/shm", ec)) {
        if (entry.path().filename().string().starts_with("xenia_memory_")) {
          std::filesystem::remove(entry.path(), ec);
        }
      }
    }
  }

  void OnPreSetup(rex::RuntimeConfig& config) override {
    CleanStaleShm();
    // Enable Xenos GPU plugin for hardware rendering via Vulkan
    if (config.gpu_plugin.empty()) {
      config.gpu_plugin = "xenos";
    }
  }

  void OnShutdown() override {
    CleanStaleShm();
  }

  void OnConfigurePaths(rex::PathConfig& paths) override {
    // If not explicitly provided via CLI, resolve relative to current directory or repo root
    if (paths.game_data_root.empty() || !std::filesystem::exists(paths.game_data_root)) {
      if (std::filesystem::exists(".local/rise360/game-base")) {
        paths.game_data_root = std::filesystem::absolute(".local/rise360/game-base");
      } else if (std::filesystem::exists("../.local/rise360/game-base")) {
        paths.game_data_root = std::filesystem::absolute("../.local/rise360/game-base");
      } else if (std::filesystem::exists("../../../.local/rise360/game-base")) {
        paths.game_data_root = std::filesystem::absolute("../../../.local/rise360/game-base");
      }
    }

    if (paths.user_data_root.empty()) {
      if (std::filesystem::exists(".local/rise360")) {
        paths.user_data_root = std::filesystem::absolute(".local/rise360/user");
      } else {
        paths.user_data_root = std::filesystem::absolute("../.local/rise360/user");
      }
    }
    if (paths.cache_root.empty()) {
      if (std::filesystem::exists(".local/rise360")) {
        paths.cache_root = std::filesystem::absolute(".local/rise360/cache");
      } else {
        paths.cache_root = std::filesystem::absolute("../.local/rise360/cache");
      }
    }
    // Per ADR-02: Base disc mode exclusively; Title Update remains quarantined.
    paths.update_data_root.clear();
  }


};
