
// Collection of DOM Elements
const $guessForm = $(".guess-form")
const $guess = $(".guess");
const $wordList = $(".words");


class BoggleGame {
    
    constructor(boardId){
        this.board = boardId
        this.words = new Set();

        // listen for submit, call handleSubmit function
        $guessForm.on("submit", this.handleSubmit.bind(this));
    }


    // show valid word in list of words
    showWord(word) {
        $(".words", this.board).append($("<li>", {text: word}));
    }

    // show status message
    showMessage(msg, cls){
        $(".msg", this.board)
            .html(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }
    
    // handle submit, check if word is valid, update score and determine message
    async handleSubmit(evt) {
        evt.preventDefault();
        let word = $guess.val();
        console.log('guess = ', word);

        // check if input is empty
        if (!word) return;

        // check locally if guess is already in word list
        if (this.words.has(word)){
            this.showMessage(`You already found ${word}`, "err")
            return;
        }

        // check server if word is valid
        const response = await axios.get("/submit", {params: {word: word}});
        console.log("response from axios= ", response)
        // let resMsg = response.data.result;
        // console.log("resMsg = ", resMsg)
        // $(".msg").html(resMsg);
        if (response.data.result === "not-word"){
            this.showMessage(`${word} is not a valid English word`, "err");
        } else if(response.data.result === "not-on-board"){
            this.showMessage(`${word} is not a valid word on the board`, "err");
        } else {
            this.showWord(word);
            this.words.add(word)
            this.showMessage(`Added: ${word}`, "ok");
        }
        $guessForm.trigger("reset");
        $guess.focus();


    };
}

let game = new BoggleGame("boggle"); 