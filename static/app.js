
// HTML References
const $guessForm = $(".guess-form")
const $guess = $(".guess");
const $wordList = $(".words-area");
const $scoreArea = $(".score-area");
const $timerArea = $(".timer-area");
const $messageArea = $(".message-area");

class BoggleGame {
    
    constructor(boardId, secs = 60){
        this.board = boardId;
        this.words = new Set();
        this.score = 0;
        this.time = secs;
        
        // display countdown
        this.countdown = setInterval(this.showTimer.bind(this), 1000);

        // listen for submit, call handleSubmit function
        $guessForm.on("submit", this.handleSubmit.bind(this));
    }

    // increments time remaining, updates DOM, calls stopTimer
    showTimer(){
        this.time--;
        $("#timer").text(this.time);
        this.stopTimer();
    }

    // runs when timer reaches 0, replaces input with "GAME OVER", shows high score
    stopTimer(){
        if (this.time < 1){
            clearInterval(this.countdown);
            $guessForm.hide();
            $timerArea.hide();
            $messageArea.hide()
            $(".below-board").prepend($('<span class="game-over">').html("GAME OVER"));
            this.endGame();
        }
    }

    async endGame(){
        await axios.post("/end-game", {score: this.score});
    }

    // show valid word in list of words
    showWord(word) {
        $($wordList, this.board).append($("<li>", {text: word}));
    }

    // show status message
    showMessage(msg){
        $(".message-area").text(msg)
    }
    
    // handle submit, check if word is valid, update score and determine message
    async handleSubmit(evt) {
        evt.preventDefault();
        let word = $guess.val();
        console.log('guess = ', word);

        // check if input is empty
        if (!word) return;

        // check if word has already been guessed
        if (this.words.has(word)){
            this.showMessage(`You already found ${word}`)
            $guessForm.trigger("reset");
            $guess.focus();
            return;
        }

        // check server if word is valid
        const response = await axios.get("/submit", {params: {word: word}});
        console.log("response from axios= ", response)
        if (response.data.result === "not-word"){
            this.showMessage(`${word} is not a word`);
        } else if(response.data.result === "not-on-board"){
            this.showMessage(`${word} is not on the board`);
        } else {
            this.showWord(word);
            this.words.add(word);
            this.showMessage(`Added: ${word}`);
            this.score += word.length;
            $scoreArea.text(`Score: ${this.score}`);

        }
        $guessForm.trigger("reset");
        $guess.focus();


    };
}

let game = new BoggleGame("boggle"); 