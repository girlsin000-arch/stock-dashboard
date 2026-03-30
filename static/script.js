let chart;

// Load companies
fetch('/companies')
.then(res => res.json())
.then(data => {
    let list = document.getElementById("companyList");

    data.forEach(c => {
        let li = document.createElement("li");
        li.innerText = c;
        li.onclick = () => loadData(c);
        list.appendChild(li);
    });
});

// Load chart data
function loadData(symbol) {
    fetch(`/data/${symbol}`)
    .then(res => res.json())
    .then(data => {

        let labels = data.map(d => d.Date);
        let prices = data.map(d => d.Close);

        if (chart) chart.destroy();

        chart = new Chart(document.getElementById("chart"), {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: symbol,
                    data: prices
                }]
            }
        });
    });
}

// Compare
function compare() {
    let s1 = document.getElementById("s1").value;
    let s2 = document.getElementById("s2").value;

    fetch(`/compare?symbol1=${s1}&symbol2=${s2}`)
    .then(res => res.json())
    .then(data => {

        if (chart) chart.destroy();

        chart = new Chart(document.getElementById("chart"), {
            type: "line",
            data: {
                labels: [...Array(data.symbol1.length).keys()],
                datasets: [
                    {
                        label: s1,
                        data: data.symbol1
                    },
                    {
                        label: s2,
                        data: data.symbol2
                    }
                ]
            }
        });
    });
}