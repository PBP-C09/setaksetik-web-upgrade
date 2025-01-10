// Helper functions of wheel
function toRad(deg){
    return deg * (Math.PI / 180.0);
}
function randomRange(min,max){
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
function easeOutSine(x) {
    return Math.sin((x * Math.PI) / 2);
}

function getPercent(input,min,max){
    return (((input - min) * 100) / (max - min))/100
}


// Script to handle spinning the wheel, updating items, and clearing all items
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const width = document.getElementById("canvas").width;
const height = document.getElementById("canvas").height;

const centerX = width / 2;
const centerY = height / 2;
const radius = width / 2;

let items = [];
let itemsDict = {};

let currentDeg = 0;
let colors = [];
let step = 360 / items.length;
let itemDegs = {};

var globalWinner = "";

document.addEventListener('DOMContentLoaded', function() {
    const categoryFilter = document.getElementById('categoryFilter');
    const defaultCategory = "All Categories";
    categoryFilter.value = defaultCategory;
    refreshOptions(defaultCategory);

    categoryFilter.addEventListener('change', function() {
        const selectedCategory = this.value;
        refreshOptions(selectedCategory);
    });
});

// Asynchronous function to refresh options based on selected category
async function refreshOptions(selectedCategory){
    document.getElementById("menuList").innerHTML = "";
    options = await getOptions(selectedCategory);

    let htmlString = "";
    options.forEach((option) => {
        const isAdded = option.fields.menu in itemsDict;
        if (selectedCategory == "All Categories" || selectedCategory == option.fields.category) {
            htmlString += `
            <div class="flex justify-between items-center p-2 pl-4 pr-4 mt-2 rounded" style="background-color: #F5F5DC">
                <span style="color: #3E2723; font-weight: bold">${option.fields.menu}</span>
                <button id="optionButton-${option.pk}" type="button" 
                        onclick="updateWheel('${option.fields.menu}', '${option.pk}', '${option.fields.restaurant_name}', '${option.fields.city}')" 
                        class="${isAdded ? 'remove-button' : 'add-button'}" 
                        style="margin-left: 0.75rem;">
                    ${isAdded ? 'Remove' : 'Add'}
                </button>
            </div>`;
        }
    });
    document.getElementById("menuList").innerHTML = htmlString;

}

// Asynchronous function to get options in json format
async function getOptions(selectedCategory){
    return fetch(`/spinthewheel/option-json/${selectedCategory}/`).then((res) => res.json())
}

// Function to add menu item to the wheel
function updateWheel(menuName, menuId, menuRestaurant, menuCity) {
    let optionButton = document.getElementById(`optionButton-${menuId}`);
    if (!(menuName in itemsDict)) {
        itemsDict[menuName] = {
            id: menuId,
            restaurant: menuRestaurant,
            city: menuCity
        }
        optionButton.innerHTML = "Remove"
        optionButton.classList.remove('add-button');
        optionButton.classList.add('remove-button');
    }
    else {
        delete itemsDict[menuName];
        optionButton.innerHTML = "Add";
        optionButton.classList.remove('remove-button');
        optionButton.classList.add('add-button');
    }

    items = Object.keys(itemsDict);
    createWheel();
}

// Function to clear all items from the wheel
function clearAll() {
    items = [];
    itemsDict = {};
    createWheel(); 

    let optionButtons = document.querySelectorAll('button[id^="optionButton-"]');
    optionButtons.forEach(optionButton => {
        optionButton.innerHTML = "Add";
        optionButton.innerHTML = "Add";
        optionButton.classList.add('option-button');
    });

    var texts = [
        "Spin aja!", 
        "Spin sekarang B)", 
        "Gachain aja gaksih :3", 
        "Putar rodanya banh~", 
        "Gausah bingung bingung laah", 
        "Sepinsetik to the rescue :D", 
        "Makan semuanya :V"
    ];

    var randomText = texts[Math.floor(Math.random() * texts.length)];
    document.getElementById("winner").innerHTML = randomText;
}


// Wheel creation script
// The source of wheel creation and spinning animation are credited to: https://youtu.be/-FNm58Z9GHM?si=F4i5fjn3LcXIv1QZ

// Function to create and update wheel settings
function createWheel() {
    const baseColors = [
    {r: 132, g: 35, b: 35},                         // 842323 (Red)
    {r: 255, g: 213, b: 79},                        // FFD54F (Yellow)
    {r: 62, g: 39, b: 35}                           // 3E2723 (Brown)
    ];

    const bufferColor = {r: 245, g: 245, b: 220};   // F5F5DC (Beige)
    colors = [];
    let numItems = items.length;
    step = 360 / numItems;

    const useBuffer = (numItems - 4) % 3 === 0;

    let colorIndex = 0;
    let patternPosition = 4;

    for (let i = 0; i < numItems; i++) {
        if (useBuffer && i + 1 === patternPosition) {
            colors.push(bufferColor);
            patternPosition += 3;
        } else {
            colors.push(baseColors[colorIndex]);
            colorIndex = (colorIndex + 1) % baseColors.length;
        }
    }
    draw();
}
draw()

// Function to draw the wheel
function draw() {
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, toRad(0), toRad(360));
    ctx.fillStyle = 'rgb(62,39,35)';
    ctx.fill();

    let startDeg = currentDeg;
    for (let i = 0; i < items.length; i++, startDeg += step) {
        let endDeg = startDeg + step

        color = colors[i]
        let colorStyle = `rgb(${color.r},${color.g},${color.b})`

        ctx.beginPath();
        rad = toRad(360/step);
        ctx.arc(centerX, centerY, radius - 2, toRad(startDeg), toRad(endDeg))
        let colorStyle2 = `rgb(${color.r - 30},${color.g - 30},${color.b - 30})`
        ctx.fillStyle = colorStyle2
        ctx.lineTo(centerX, centerY);
        ctx.fill()

        ctx.beginPath();
        rad = toRad(360/step);
        ctx.arc(centerX, centerY, radius - 30, toRad(startDeg), toRad(endDeg))
        ctx.fillStyle = colorStyle
        ctx.lineTo(centerX, centerY);
        ctx.fill()

        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(toRad((startDeg + endDeg)/2));
        ctx.textAlign = "center";
        if(color.r > 150 || color.g > 150 || color.b > 150){
            ctx.fillStyle = "#000";
        }
        else{
            ctx.fillStyle = "#fff";
        }
        ctx.font = '20px Raleway';
        ctx.fillText(items[i].substring(0, 17), 130, 10);
        ctx.restore();

        itemDegs[items[i]] = 
            {
            "startDeg": startDeg,
            "endDeg" : endDeg
            }
        

        // Check winner
        let startDegModulo = startDeg % 360;
        let endDegModulo = endDeg % 360;

        // Check if the white triangle (0 degrees) is between this segment's start and end
        if ((startDegModulo < endDegModulo && 0 >= startDegModulo && 0 <= endDegModulo) || 
            (startDegModulo > endDegModulo && (0 >= startDegModulo || 0 <= endDegModulo))) {
            globalWinner = items[i];
            document.getElementById("winner").innerHTML = globalWinner;
        }

    }
}

// Spinning logic
let speed = 0;
let maxRotation = randomRange(360 * 3, 360 * 6);
let pause = false;

// Function to animate the wheel
function animate() {
    if (pause) return

    speed = easeOutSine(getPercent(currentDeg, maxRotation, 0)) * 20;
    if (speed < 0.01) {
        speed = 0;
        pause = true;
        
        showWinnerModal(globalWinner);

    }
    currentDeg += speed;
    draw();
    window.requestAnimationFrame(animate);
    
}

// Function to spin the wheel
function spin() {
    if (items.length != 0) {
        if(speed != 0){
            return
        }

        currentDeg = 0
        
        maxRotation = randomRange(360 * 3, 360 * 6)
        pause = false
        window.requestAnimationFrame(animate);
    }
}


// Script to show winner and add to history with AJAX
const addSpinHistoryBtn = document.getElementById("addSpinHistoryBtn");
const closeModalBtn = document.getElementById("closeModalBtn");

// Function to show winner modal
function showWinnerModal(winnerName) {
    document.getElementById("winnerName").innerText = winnerName;
    document.getElementById("winnerRestaurant").innerText = itemsDict[winnerName]["restaurant"];
    document.getElementById("winnerCity").innerText = itemsDict[winnerName]["city"];
    document.getElementById("winnerModal").classList.remove("hidden");
}

// Function to hide winner modal
function hideWinnerModal() {
    document.getElementById("winnerModal").classList.add("hidden");
}

// Function to add spin history
function addSpinHistory() {
    const formData = new FormData();
    const winnerId = itemsDict[globalWinner]['id'];
    const note = document.getElementById("note").value || "-"

    formData.append("winner", globalWinner);
    formData.append("winnerId", winnerId);
    formData.append("note", note)

    fetch(addSpinHistoryUrl, {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
        }        
    })
    .then(response => refreshSpinHistory())

    document.getElementById("note").value = ""
    return false;
}

var ngitung = 0
// Asynchronous function to refresh spin history
async function refreshSpinHistory() {
    document.getElementById("spin-history-container").innerHTML = "";
    document.getElementById("spin-history-container").className = "";
    const spinHistory = await getSpinHistory();
    let htmlString = `
    <h1 class="text-4xl text-center">
        Yang <span class="italic">pernah</span> kamu spin
    </h1>    
    <div class="border-t-2 border-[beige] mt-3 mx-auto w-2/3"></div>`;
    let classNameString = "";

    if (spinHistory.length === 0) {
        htmlString = ""
    }
    else {
        classNameString = "mt-24 columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6 w-full"
        spinHistory.forEach((history) => {
            htmlString += `
            <div class="relative break-inside-avoid">
                <div class="relative top-5 bg-[#FFD54F] shadow-md rounded-lg mb-6 break-inside-avoid flex flex-col border-2 border-[#3E2723] transform rotate-1 hover:rotate-0 transition-transform duration-300">
                    <div class="bg-[#F5F5DC] text-[#3E2723] p-4 rounded-t-lg border-b-2 border-[#3E2723] text-center">
                        <h3 class="font-bold text-x1 mb-1" style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 26px">${history.fields.winner}</h3>
                        <p class="text-[#3E2723]">Di-<span style="font-style: italic">spin</span> pada: ${history.fields.spin_time}</p>
                        <p class="text-[#3E2723]"><span style="font-style: italic">Note</span>: ${history.fields.note}</p>
                    </div>
                    <div class="p-3 flex justify-between items-center gap-1">
                        <button class="hover:text-[#F5F5DC] text-[#842323] rounded-lg px-4 py-2 transition duration-300 ml-6" style="font-family: 'Playfair Display', serif; font-style: italic; font-weight: bold;" onclick="window.location.href='/booking/form/${history.fields.winnerId}'">
                        Book
                        </button>
                        <button class="hover:text-[#F5F5DC] text-[#842323] rounded-lg px-4 py-2 transition duration-300" style="font-family: 'Playfair Display', serif; font-style: italic; font-weight: bold;" onclick="window.location.href='/explore/menu_detail/${history.fields.winnerId}'">
                        Detail
                        </button>
                        <button class="hover:text-[#F5F5DC] text-[#842323] rounded-lg px-4 py-2 transition duration-300 mr-6" style="font-family: 'Playfair Display', serif; font-style: italic; font-weight: bold;" onclick="deleteSpinHistory('${history.pk}')">
                        Hapus
                        </button>
                    </div>
                </div>
            </div>
            `;
        });
    }
    document.getElementById("spin-history-container").className = classNameString;
    document.getElementById("spin-history-container").innerHTML = htmlString;
}
refreshSpinHistory();

// Asynchronous function to get spin history in json format
async function getSpinHistory(){
    return fetch(historyJsonUrl).then((res) => res.json())
}

// Asynchronous function to delete spin history based on primary key
async function deleteSpinHistory(pk) {
    const response = await fetch(`/spinthewheel/delete/${pk}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    if (response.ok) {
        refreshSpinHistory();
    } else {
        console.error("Error deleting spin history:", response.statusText);
    }
}

// Event listener for the click of addSpinHistoryBtn
document.getElementById("addSpinHistoryBtn").addEventListener("click", () => {
    addSpinHistory();
    hideWinnerModal();
});

// Function to get cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}