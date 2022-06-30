class BoggleGame {
    
    constructor(boardId){
        this.board = boardId

        // listen for submit, call handleSubmit function
        $(".guess-form").on("submit", this.handleSubmit.bind(this));
    }



    // show valid word in list of words
    showWord(word) {
        $(".words", this.board).append($("<li>", {text: word}));
    }

    // handle submit, check if word is valid, update score and list word or display error
    async handleSubmit(evt) {
        evt.preventDefault();
        const $guess = $("#guess").val();
        console.log('guess = ', $guess);

        // check locally input is empty
        if (!$guess) return;

        // check locally if guess is already in word list
        // if (this.words.has($guess)){
        //     this.showMessage(`You already found ${$guess}`, "err")
        //     return;
        // }

        // check server if word is valid
        const response = await axios.get("/submit", {params: {word: guess}});
        console.log("response from axios= ", response)
        if (response.data.result === "not-word"){
            this.showMessage(`${guess} is not a valid English word`, "err");
        } else if(response.data.result === "not-on-board"){
            this.showMessage(`${guess} is not a valid word on the board`, "err");
        } else {
            this.showWord(guess);
        }

    };
}