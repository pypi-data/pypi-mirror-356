def build_pod_spec(pod_name: str, image: str) -> dict:
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": pod_name,
            "namespace": "default"
        },
        "spec": {
            "volumes": [
                {"name": "kfd", "hostPath": {"path": "/dev/kfd", "type": "CharDevice"}},
                {"name": "dri", "hostPath": {"path": "/dev/dri", "type": "Directory"}},
                {"name": "workspace", "emptyDir": {}}
            ],
            "containers": [
                {
                    "name": "torch-container",
                    "image": image,
                    "command": ["/bin/bash", "-c"],
                    "args": [
                        "export PYTHONPATH=/workspace && "
                        "python -c \"import torch_shim; exec(open('app.py').read())\""
                    ],
                    "stdin": True,
                    "tty": True,
                    "volumeMounts": [
                        {"name": "kfd", "mountPath": "/dev/kfd"},
                        {"name": "dri", "mountPath": "/dev/dri"},
                        {"name": "workspace", "mountPath": "/workspace"}
                    ],
                    "ports": [
                        {"containerPort": 7860, "name": "gradio"},
                        {"containerPort": 8000, "name": "fastapi"}
                    ],
                    "securityContext": {
                        "privileged": True,
                        "runAsUser": 0,
                        "runAsGroup": 0,
                        "capabilities": {"add": ["SYS_PTRACE"]}
                    }
                }
            ],
            "restartPolicy": "Always",
            "imagePullSecrets": [
                {"name": "gcp-docker-virtual"},
                {"name": "gcr-json-key"}
            ],
            "tolerations": [
                {
                    "key": "node.kubernetes.io/not-ready",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300
                },
                {
                    "key": "node.kubernetes.io/unreachable",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300
                }
            ]
        }
    }