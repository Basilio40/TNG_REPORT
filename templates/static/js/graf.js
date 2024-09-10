function renderiza_faturamento(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('faturamento_mensal').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: data.dado2,
                    backgroundColor: [
                        'rgba(83 , 83, 236)',
                        'rgba(64, 206, 255)',
                      ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


    })


    

}

function renderiza_custos(url){

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        const ctx = document.getElementById('custo_mensal').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Consumo','Demanda','Penalidades','Outros','Iluminação Publica'],
                datasets: [{
                    label: 'Despesas',
                    data: data.dado2,
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                }
            
        });


    })
  
}

function renderiza_historico_fatura(url){

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('historico_fatura').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.mes,
                datasets: [{
                    label: data.ano,
                    data: data.valor,
                    backgroundColor: [
                        'rgba(64, 206, 255)',
                      ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


    })


    

}

function renderiza_demanda_mensal(url){

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('demanda_mensal').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.mes,
                datasets: [{
                    label: data.ano,
                    data: data.valor,
                    backgroundColor: [
                        'rgba(64, 206, 255)',
                      ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


    })

}

function renderiza_economia_total(url){

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('economia_total').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['cativo','livre','economia'],
                datasets: [{
                    data: data.econ,
                    backgroundColor: [
                        'rgba(15, 77, 162)',
                        'rgba(40, 144, 207)',
                        'rgba(107, 200, 181)',
                      ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


    })

}

function renderiza_econ_fat(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('faturamento_total').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: data.fat_t,
                    backgroundColor: [
                        'rgba(15, 77, 162)',
                        'rgba(107, 200, 181)',
                      ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


    })


    

}

function renderiza_percent(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('percentagem').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: data.percent,
                    backgroundColor: [
                        'rgba(15, 77, 162)',
                        'rgba(107, 200, 181)',
                      ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


    })


    

}


