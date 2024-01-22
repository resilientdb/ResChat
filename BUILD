package(default_visibility = ["//visibility:public"])
cc_library(
    name = "pybind_kv_service",
    srcs = ["pybind_kv_service.cpp"],
    deps = [
        "@com_resdb_nexres//common/proto:signature_info_cc_proto",
        "@com_resdb_nexres//interface/kv:kv_client",
        "@com_resdb_nexres//platform/config:resdb_config_utils",
        "@pybind11//:pybind11",
    ],
)
