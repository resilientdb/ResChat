package(default_visibility = ["//visibility:public"])
cc_binary(
    name = "pybind_aes.so",
    srcs = ["aes_encryption.cpp"],
    linkshared = 1,
    linkstatic = 1,
    linkopts = [
        "-lssl",   # 链接 OpenSSL 库
        "-lcrypto", # 链接 OpenSSL 的 crypto 库
    ],
    deps = [
        "@pybind11//:pybind11",
    ],
)
py_library(
    name = "pybind_aes_so",
    data = [":pybind_aes.so"],
    imports = ["."],
)

