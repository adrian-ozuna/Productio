const generateRndmColor = () => {
    return `#${Math.floor(Math.random()*16777215).toString(16)}`
}

const assignGeneratedColor = () => {
    const cards = document.getElementsByClassName('card')
    for(const card of cards) {
        card.style.borderColor = generateRndmColor()
    }
}

assignGeneratedColor()