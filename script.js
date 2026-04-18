// Show only the selected section and hide the others
function showSection(sectionId) {
    const sections = document.querySelectorAll(".content-section");

    sections.forEach(function (section) {
        section.classList.remove("active");
    });

    document.getElementById(sectionId).classList.add("active");
}
