// index_script.js

// List of valid building names and alternate names
const buildings = {
    "administration building": ["admin", "admin building", "administration"],
    "biological sciences building": ["bio sci", "biology", "biological sciences"],
    "commons": ["the commons"],
    "engineering building": ["engineering"],
    "fine arts building": ["fa", "fine arts"],
    "information and technology/engineering building": ["it", "ite", "information and technology"],
    "interdisciplinary life sciences building": ["interdisciplinary life sciences", "ilsb"],
    "lecture hall 1": ["lh1"],
    "library & gallery, albin o. kuhn": ["library", "aok"],
    "math and psychology building": ["math and psychology", "math and psych"],
    "meyerhoff chemistry building": ["meyrhoff"],
    "performing arts and humanities": ["performing arts", "humanities"],
    "physics building": ["physics"],
    "public policy building": ["public policy", "pb"],
    "retriever activities center": ["rac"],
    "sherman hall": ["sherman"],
    "sondheim hall": ["sondheim"],
    "the center for well-being": ["rih", "the center for wellbeing"],
    "true grit’s": ["dining hall", "true grits"],
    "university center": ["uc"]
};

// Normalize input: lowercase + remove spaces
// Makes the validation case insensitive and accounts for any spacing users may use
function normalize(input) {
    return input.toLowerCase().replace(/\s/g, "");
}

// Validate a building input
function isValidBuilding(input) {
    const normInput = normalize(input);
    return Object.keys(buildings).some(mainName => {
        if (normalize(mainName) === normInput) return true;
        return buildings[mainName].some(alias => normalize(alias) === normInput);
    });
}

// Form validation
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const startInput = document.getElementById("start_dest");
    const endInput = document.getElementById("end_destination");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Stop form from submitting

        const start = startInput.value.trim();
        const end = endInput.value.trim();
        let errors = [];

        if (!start) errors.push("Starting location is required.");
        else if (!isValidBuilding(start)) errors.push(`"${start}" is not a valid building.`);

        if (!end) errors.push("Ending location is required.");
        else if (!isValidBuilding(end)) errors.push(`"${end}" is not a valid building.`);

        if (errors.length > 0) {
            alert(errors.join("\n"));
            return false;
        }

        // For now, just log to console (later integrate backend)
        console.log("Start:", start);
        console.log("End:", end);

        // TODO: Connect to backend
    });
});
