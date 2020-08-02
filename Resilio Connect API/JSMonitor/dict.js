var dict = {
    dog: "booey",
    cat:"dumb",
    fish: "watery",
};

dict["horse"]= "happy";

var name = dict["dog"];
console.log(name)

var second = {
    snake: "fat"
};

var bob = {
    joe: "unglyr"
}
console.log(dict.hasOwnProperty("dog"));


dict["joe"] = second

console.log(second["snake"]);

