pragma solidity ^0.2.0;

contract MedStats {
    final address hospital;
    uint count;
    mapping(address => bool) risk;

    constructor() public {
        hospital = me;
        count = 0;
    }

    function record(address pat, bool r) public {
        require(hospital == me);
        risk[pat] = r;
        count = count + (r ? 1 : 0);
    }

    function check(bool r){
        require(r == risk[me]);
    }

}