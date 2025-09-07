import resource
import tempfile
import subprocess

def Limit_resource():
    mem = 50*1024*1024
    resource.setrlimit(resource.RLIMIT_CPU,(2,2))
    resource.setrlimit(resource.RLIMIT_AS,(mem,mem))

def runcode_subprocess(code):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as f:
        f.write(code)
        f.flush() 

        try:
            proc = subprocess.run(
                ["python3", f.name],
                text=True,
                timeout=5,       
                capture_output=True 
            )
            result = {
                "ok": proc.returncode == 0,
                "stdout": proc.stdout,
                "stderr": proc.stderr
            }
        except subprocess.TimeoutExpired:
            result = {
                "ok": False,
                "stdout": "",
                "stderr": "Timeout: code chạy quá 5 giây"
            }
        except Exception as e:
            result = {
                "ok": False,
                "stdout": "",
                "stderr": f"Lỗi khi chạy subprocess: {e}"
            }

    return result