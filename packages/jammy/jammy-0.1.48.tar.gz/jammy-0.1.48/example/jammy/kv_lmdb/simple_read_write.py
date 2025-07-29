# pylint: skip-file
from jammy.storage.kv.lmdb import LMDBKVStore


def main():
    kv = LMDBKVStore("/tmp/test_1.lmdb", readonly=False)

    kv.put("a", 1)
    kv.put("b", 2)

    assert "a" in kv and kv["a"] == 1
    assert "b" in kv and kv["b"] == 2
    assert "c" not in kv

    for k in kv.keys():
        print(k, kv[k])


if __name__ == "__main__":
    main()
