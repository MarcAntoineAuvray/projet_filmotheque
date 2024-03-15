document.addEventListener("DOMContentLoaded", function() {
    const submitButton = document.getElementById("submitButton") as HTMLButtonElement;
    const textInput = document.getElementById("textInput") as HTMLInputElement;
    const displayArea = document.getElementById("displayArea");

    if (submitButton && textInput && displayArea) {
        submitButton.addEventListener("click", function() {
            const enteredText = textInput.value;
            displayArea.textContent = enteredText;
        });
    }
});
