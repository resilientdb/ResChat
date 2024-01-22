#include <fcntl.h>
#include <getopt.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <pybind11/pybind11.h>

#include <fstream>
#include "common/proto/signature_info.pb.h"
#include "interface/kv/kv_client.h"
#include "platform/config/resdb_config_utils.h"

using resdb::GenerateReplicaInfo;
using resdb::GenerateResDBConfig;
using resdb::KVClient;
using resdb::ReplicaInfo;
using resdb::ResDBConfig;

auto kv(char** command) {
    ResDBConfig config = GenerateResDBConfig("kv_server.conf");
    config.SetClientTimeoutMs(100000);
    KVClient client(config);
    std::string cmd = command[0];
    std::string key = command[1];

    if(cmd == "get") {
        auto result = client.Get(key);
        if (result == nullptr) {
            printf("client get value fail\n");
        } else {
            return result;
        }
    } else if(cmd == "set") {
        std::string value = command[2];
        int result = client.Set(key, value);
        printf("set key = %s, value = %s done, result = %d\n", key.c_str(), value.c_str(), result);
    }
}

PYBIND11_MODULE(pybind_kv, m) {
    m.def("kv", &kv, "set or get operation");
}

