#include <iostream>
#include <cpprest/http_client.h>
#include <cpprest/json.h>
#include <cpprest/uri.h>
#include <cpprest/ws_client.h>
#include <cpprest/streams.h>
#include <discord_rpc.h>
#include <windows.h>
#include <psapi.h>
#include <pymem.h>
#include <regex>
#include <string>
#include <vector>
#include <unordered_map>

#pragma comment(lib, "discord-rpc.lib")
#pragma comment(lib, "pymem.lib")

using namespace std;
using namespace web;
using namespace web::http;
using namespace web::http::client;

class Information {
public:
    std::tuple<std::string, std::string, std::string> get_data() {
        auto user_id = read_id();
        auto response = get_user_data(user_id).get();
        auto data = response.extract_json().get();
        auto avatar = data["data"]["attributes"]["avatarUrl"].as_string();
        auto name = data["data"]["attributes"]["displayName"].as_string();
        auto realname = data["data"]["attributes"]["username"].as_string();
        return std::make_tuple(avatar, name, realname);
    }

private:
    int read_id() {
        auto config_path = "C:/RPC/settings.json";
        if (!std::filesystem::exists(config_path)) {
            std::cout << "Config file not found." << std::endl;
            return -1;
        }
        std::ifstream configfile(config_path);
        json::value data;
        configfile >> data;
        auto user_id = data["ForumID"].as_integer();
        return user_id;
    }

    pplx::task<http_response> get_user_data(int user_id) {
        http_client client(U("https://forum.wayzer.ru"));
        uri_builder builder(U("/api/users/" + std::to_string(user_id)));
        return client.request(methods::GET, builder.to_string());
    }
};

class Mr_Freeman {
public:
    void Mr_Freeman() {
        std::string url = "https://youtu.be/1snyDYHnkL8";
        ShellExecuteA(nullptr, "open", url.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
    }

    bool terminate_process() {
        auto pid = ServerStatus().is_runnig();
        if (pid == 0) {
            std::cout << "Process not found." << std::endl;
            return false;
        }
        HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
        if (hProcess == NULL) {
            std::cout << "Failed to open process." << std::endl;
            return false;
        }
        if (!TerminateProcess(hProcess, 0)) {
            std::cout << "Failed to terminate process." << std::endl;
            CloseHandle(hProcess);
            return false;
        }
        CloseHandle(hProcess);
        return true;
    }
};

class ServerStatus {
public:
    ServerStatus() {
        server_list = {
            {"46.174.54.203", {"Riverton", "riverton"}},
            {"46.174.54.52", {"Minton", "minton"}},
            {"37.230.228.180", {"Carlin", "carlin"}},
            {"62.122.213.48", {"Brooks", "brooks"}},
            {"37.230.162.208", {"Rockford", "rockford"}}
        };
    }

    DWORD is_runnig() {
        DWORD pid = 0;
        std::vector<std::string> processes = {"gmod.exe", "hl2.exe"};
        for (const auto& process : processes) {
            pymem::process pm(process);
            if (pm.is_running()) {
                pid = pm.pid();
                break;
            }
        }
        return pid;
    }

    int get_online(const std::string& ip) {
        auto c = a2s::info({ip, 27015});
        return c.players();
    }

    std::tuple<std::string, std::string, int> get_status() {
        auto pid = is_runnig();
        if (pid == 0) return {};
        pymem::process gmod("hl2.exe", pid);
        auto client = gmod.find_module("engine.dll");
        if (client == pymem::module::null()) return {};
        auto ip = std::regex_search(gmod.read<std::string>(client.lpBaseOfDll + OFS1, 14), ip_regex);
        if (!ip) return {};
        auto ip_address = ip.str(0);
        auto it = server_list.find(ip_address);
        if (it == server_list.end()) {
            Mr_Freeman().Mr_Freeman();
            Mr_Freeman().terminate_process();
            return {};
        }
        auto cd = gmod.read<std::string>(client.lpBaseOfDll + OFS2, 100);
        if (cd.find("disconnect") != std::string::npos) return {};
        std::string status = (cd.find("connect") != std::string::npos) ? "Заходит на" : "Играет на";
        return {status + " " + it->second.first, it->second.second, get_online(ip_address)};
    }

private:
    const DWORD OFS1 = 0x5B47CC;
    const DWORD OFS2 = 0x7DC1C0;
    std::unordered_map<std::string, std::pair<std::string, std::string>> server_list;
    std::regex ip_regex{"\\d+\\.\\d+\\.\\d+\\.\\d+"};
};

void handle_discord_ready(const DiscordUser* request) {
    std::cout << "Discord Rich Presence is ready." << std::endl;
}

int main() {
    DiscordEventHandlers handlers;
    memset(&handlers, 0, sizeof(handlers));
    Discord_Initialize("1237037992368148490", &handlers, 1, nullptr);
    Information info;
    auto [avatar, name, realname] = info.get_data();
    auto button = std::vector<DiscordButton>{
        {"Github", "https://github.com/v1lmok/RPC_WRP"},
        {"Forum", "https://forum.wayzer.ru/u/" + realname}
    };
    auto time_start = std::time(nullptr);
    ServerStatus ss;
    while (true) {
        auto [status, img, lt] = ss.get_status();
        if (status.empty()) {
            img = "wrp";
            lt = "WayZer RolePlay";
        }
        DiscordRichPresence discordPresence{};
        discordPresence.state = "Мой ник на форуме " + name;
        discordPresence.details = status;
        discordPresence.largeImageKey = img.c_str();
        discordPresence.largeImageText = std::to_string(lt) + "/128";
        discordPresence.smallImageKey = avatar.c_str();
        discordPresence.smallImageText = name.c_str();
        discordPresence.startTimestamp = time_start;
        Discord_UpdatePresence(&discordPresence);
        Sleep(15000);
    }
    Discord_Shutdown();
    return 0;
}
#include <iostream>
#include <cpprest/http_client.h>
#include <cpprest/json.h>
#include <cpprest/uri.h>
#include <cpprest/ws_client.h>
#include <cpprest/streams.h>
#include <discord_rpc.h>
#include <windows.h>
#include <psapi.h>
#include <pymem.h>
#include <regex>
#include <string>
#include <vector>
#include <unordered_map>

#pragma comment(lib, "discord-rpc.lib")
#pragma comment(lib, "pymem.lib")

using namespace std;
using namespace web;
using namespace web::http;
using namespace web::http::client;

class Information {
public:
    std::tuple<std::string, std::string, std::string> get_data() {
        auto user_id = read_id();
        auto response = get_user_data(user_id).get();
        auto data = response.extract_json().get();
        auto avatar = data["data"]["attributes"]["avatarUrl"].as_string();
        auto name = data["data"]["attributes"]["displayName"].as_string();
        auto realname = data["data"]["attributes"]["username"].as_string();
        return std::make_tuple(avatar, name, realname);
    }

private:
    int read_id() {
        auto config_path = "C:/RPC/settings.json";
        if (!std::filesystem::exists(config_path)) {
            std::cout << "Config file not found." << std::endl;
            return -1;
        }
        std::ifstream configfile(config_path);
        json::value data;
        configfile >> data;
        auto user_id = data["ForumID"].as_integer();
        return user_id;
    }

    pplx::task<http_response> get_user_data(int user_id) {
        http_client client(U("https://forum.wayzer.ru"));
        uri_builder builder(U("/api/users/" + std::to_string(user_id)));
        return client.request(methods::GET, builder.to_string());
    }
};

class Mr_Freeman {
public:
    void Mr_Freeman() {
        std::string url = "https://youtu.be/1snyDYHnkL8";
        ShellExecuteA(nullptr, "open", url.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
    }

    bool terminate_process() {
        auto pid = ServerStatus().is_runnig();
        if (pid == 0) {
            std::cout << "Process not found." << std::endl;
            return false;
        }
        HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
        if (hProcess == NULL) {
            std::cout << "Failed to open process." << std::endl;
            return false;
        }
        if (!TerminateProcess(hProcess, 0)) {
            std::cout << "Failed to terminate process." << std::endl;
            CloseHandle(hProcess);
            return false;
        }
        CloseHandle(hProcess);
        return true;
    }
};

class ServerStatus {
public:
    ServerStatus() {
        server_list = {
            {"46.174.54.203", {"Riverton", "riverton"}},
            {"46.174.54.52", {"Minton", "minton"}},
            {"37.230.228.180", {"Carlin", "carlin"}},
            {"62.122.213.48", {"Brooks", "brooks"}},
            {"37.230.162.208", {"Rockford", "rockford"}}
        };
    }

    DWORD is_runnig() {
        DWORD pid = 0;
        std::vector<std::string> processes = {"gmod.exe", "hl2.exe"};
        for (const auto& process : processes) {
            pymem::process pm(process);
            if (pm.is_running()) {
                pid = pm.pid();
                break;
            }
        }
        return pid;
    }

    int get_online(const std::string& ip) {
        auto c = a2s::info({ip, 27015});
        return c.players();
    }

    std::tuple<std::string, std::string, int> get_status() {
        auto pid = is_runnig();
        if (pid == 0) return {};
        pymem::process gmod("hl2.exe", pid);
        auto client = gmod.find_module("engine.dll");
        if (client == pymem::module::null()) return {};
        auto ip = std::regex_search(gmod.read<std::string>(client.lpBaseOfDll + OFS1, 14), ip_regex);
        if (!ip) return {};
        auto ip_address = ip.str(0);
        auto it = server_list.find(ip_address);
        if (it == server_list.end()) {
            Mr_Freeman().Mr_Freeman();
            Mr_Freeman().terminate_process();
            return {};
        }
        auto cd = gmod.read<std::string>(client.lpBaseOfDll + OFS2, 100);
        if (cd.find("disconnect") != std::string::npos) return {};
        std::string status = (cd.find("connect") != std::string::npos) ? "Заходит на" : "Играет на";
        return {status + " " + it->second.first, it->second.second, get_online(ip_address)};
    }

private:
    const DWORD OFS1 = 0x5B47CC;
    const DWORD OFS2 = 0x7DC1C0;
    std::unordered_map<std::string, std::pair<std::string, std::string>> server_list;
    std::regex ip_regex{"\\d+\\.\\d+\\.\\d+\\.\\d+"};
};

void handle_discord_ready(const DiscordUser* request) {
    std::cout << "Discord Rich Presence is ready." << std::endl;
}

int main() {
    DiscordEventHandlers handlers;
    memset(&handlers, 0, sizeof(handlers));
    Discord_Initialize("1237037992368148490", &handlers, 1, nullptr);
    Information info;
    auto [avatar, name, realname] = info.get_data();
    auto button = std::vector<DiscordButton>{
        {"Github", "https://github.com/v1lmok/RPC_WRP"},
        {"Forum", "https://forum.wayzer.ru/u/" + realname}
    };
    auto time_start = std::time(nullptr);
    ServerStatus ss;
    while (true) {
        auto [status, img, lt] = ss.get_status();
        if (status.empty()) {
            img = "wrp";
            lt = "WayZer RolePlay";
        }
        DiscordRichPresence discordPresence{};
        discordPresence.state = "Мой ник на форуме " + name;
        discordPresence.details = status;
        discordPresence.largeImageKey = img.c_str();
        discordPresence.largeImageText = std::to_string(lt) + "/128";
        discordPresence.smallImageKey = avatar.c_str();
        discordPresence.smallImageText = name.c_str();
        discordPresence.startTimestamp = time_start;
        Discord_UpdatePresence(&discordPresence);
        Sleep(15000);
    }
    Discord_Shutdown();
    return 0;
}
