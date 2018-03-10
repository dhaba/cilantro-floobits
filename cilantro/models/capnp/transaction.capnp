@0x8cff3844f3101ec9;

struct MetaData {
    proof @0 :Data;
    signature @1 :Data;
    nonce @2 :Data;
    timestamp @3 :Float32;
}

struct StandardTransaction {
    metadata @0 :MetaData;
    payload @1 :Payload;

    struct Payload {
        sender @0 :Data;
        receiver @1 :Data;
        amount @2 :UInt64;
    }
}
