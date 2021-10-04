pragma solidity ^0.8.0;

contract SimpleStorage{

    uint256 public favouriteNumber;
    bool favouriteBool;

    struct People{
        uint256 favouriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;

    function addPerson(string memory _name, uint256 _favouriteNumber)public{
        people.push(People({favouriteNumber: _favouriteNumber, name: _name}));
        nameToFavouriteNumber[_name] = _favouriteNumber;

    }

    function store(uint256 _favouriteNumber)public{
        favouriteNumber = _favouriteNumber;
    }

    function retrieve() public view returns(uint256){
        return favouriteNumber;
        
    }

    

}




