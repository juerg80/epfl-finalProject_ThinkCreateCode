// top score
let fieldInfo=document.getElementById("comment_topScore");
let fieldTopScore=document.getElementById("field_topScore");
let fieldCurrentScore=document.getElementById("cashAccount");
let buttonResetScore=document.getElementById("bt_ResetTopScore");

// define some functions
function readScore(){
    let Score=localStorage.getItem("TopScore");
    return Score
}

function readCurrentScore(){
    raw=fieldCurrentScore.innerText;
    finalString=raw.replace("Current Cash: ","");
    finalFloat=parseFloat(finalString)
    return finalFloat
}

function resetScore(){
    localStorage.setItem("TopScore",0);
    location.reload()
}

function updateMessage(message){
    fieldInfo.value=message;
}

function updateScore(score){
    fieldTopScore.value=score;
}

function compareCurrentVsTopScore(){
    let msg="";
    let top=readScore();
    let current=readCurrentScore();

    if (current >= top){
        msg="You rock! New topScore! Congratulations"
        localStorage.setItem("TopScore",current)
    }
    else{
        msg="You're still below top score...try harder!"
    }
    return msg
}

// add listener
buttonResetScore.addEventListener("click",resetScore)

document.onload = updateScore(readScore()) 
document.onload = updateMessage(compareCurrentVsTopScore())


