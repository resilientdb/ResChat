import sys
sys.path.append("bazel-out/k8-fastbuild/bin/")
import pybind_kv

pybind_kv.set("test", "123", "/home/ubuntu/Desktop/incubator-resilientdb/scripts/deploy/config_out/client.config")
print(pybind_kv.get("test", "/home/ubuntu/Desktop/incubator-resilientdb/scripts/deploy/config_out/client.config"))





