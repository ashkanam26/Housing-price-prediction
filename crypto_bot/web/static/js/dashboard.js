// Crypto Trading Bot Dashboard JavaScript

let priceChart = null;
let updateInterval = null;

// Initialize chart
function initializeChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Price',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 3,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Log message to console
function logMessage(message, type = 'info') {
    const logConsole = document.getElementById('logConsole');
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    logConsole.appendChild(logEntry);
    logConsole.scrollTop = logConsole.scrollHeight;
}

// Update status indicator
function updateStatus(status, text) {
    const indicator = document.querySelector('.status-dot');
    const statusText = document.getElementById('statusText');
    
    indicator.className = 'status-dot';
    if (status === 'active') {
        indicator.classList.add('active');
    } else if (status === 'training') {
        indicator.classList.add('training');
    } else if (status === 'error') {
        indicator.classList.add('error');
    }
    
    statusText.textContent = text;
}

// Initialize bot
async function initializeBot() {
    const symbol = document.getElementById('symbol').value;
    const capital = parseFloat(document.getElementById('capital').value);
    const timeframe = document.getElementById('timeframe').value;
    
    logMessage('Initializing bot...', 'info');
    
    try {
        const response = await fetch('/api/initialize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol,
                initial_capital: capital,
                timeframe: timeframe,
                lookback: 60
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            logMessage('Bot initialized successfully!', 'success');
            updateStatus('training', 'Initialized');
            document.getElementById('trainBtn').disabled = false;
        } else {
            logMessage(`Error: ${data.message}`, 'error');
            updateStatus('error', 'Error');
        }
    } catch (error) {
        logMessage(`Error: ${error.message}`, 'error');
        updateStatus('error', 'Error');
    }
}

// Train models
async function trainModels() {
    logMessage('Training models... This may take a moment.', 'info');
    updateStatus('training', 'Training');
    
    try {
        const response = await fetch('/api/train', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ periods: 500 })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            logMessage('Models training started!', 'success');
            
            // Check status periodically
            setTimeout(checkTrainingStatus, 3000);
        } else {
            logMessage(`Error: ${data.message}`, 'error');
            updateStatus('error', 'Error');
        }
    } catch (error) {
        logMessage(`Error: ${error.message}`, 'error');
        updateStatus('error', 'Error');
    }
}

// Check training status
async function checkTrainingStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.model_trained) {
            logMessage('Models trained successfully!', 'success');
            updateStatus('active', 'Ready');
            document.getElementById('startBtn').disabled = false;
        } else {
            setTimeout(checkTrainingStatus, 2000);
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Start bot
async function startBot() {
    logMessage('Starting trading bot...', 'info');
    
    try {
        const response = await fetch('/api/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                iterations: 100,
                interval: 60
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            logMessage('Bot started!', 'success');
            updateStatus('active', 'Running');
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            
            // Start updating dashboard
            startDashboardUpdates();
        } else {
            logMessage(`Error: ${data.message}`, 'error');
        }
    } catch (error) {
        logMessage(`Error: ${error.message}`, 'error');
    }
}

// Stop bot
async function stopBot() {
    logMessage('Stopping bot...', 'info');
    
    try {
        const response = await fetch('/api/stop', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            logMessage('Bot stopped!', 'warning');
            updateStatus('training', 'Stopped');
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            
            // Stop updating dashboard
            stopDashboardUpdates();
        } else {
            logMessage(`Error: ${data.message}`, 'error');
        }
    } catch (error) {
        logMessage(`Error: ${error.message}`, 'error');
    }
}

// Start dashboard updates
function startDashboardUpdates() {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
    
    updateDashboard();
    updateInterval = setInterval(updateDashboard, 5000);
}

// Stop dashboard updates
function stopDashboardUpdates() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

// Update dashboard
async function updateDashboard() {
    try {
        // Update analysis
        const analysisResponse = await fetch('/api/analysis');
        if (analysisResponse.ok) {
            const analysisData = await analysisResponse.json();
            updateMarketAnalysis(analysisData);
            updateChart(analysisData.chart_data);
        }
        
        // Update performance
        const perfResponse = await fetch('/api/performance');
        if (perfResponse.ok) {
            const perfData = await perfResponse.json();
            updatePerformanceMetrics(perfData.performance);
            updateRecentTrades(perfData.trades);
        }
        
        // Update status
        const statusResponse = await fetch('/api/status');
        if (statusResponse.ok) {
            const statusData = await statusResponse.json();
            updateCurrentPosition(statusData.position);
        }
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
}

// Update market analysis
function updateMarketAnalysis(data) {
    const container = document.getElementById('marketAnalysis');
    
    const html = `
        <div class="analysis-item">
            <span class="analysis-label">Current Price:</span>
            <span class="analysis-value">$${data.current_price.toFixed(2)}</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Price Signal:</span>
            <span class="analysis-value signal-${data.price_signal.toLowerCase()}">${data.price_signal}</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Sentiment Signal:</span>
            <span class="analysis-value signal-${data.sentiment_signal.toLowerCase()}">${data.sentiment_signal}</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Combined Signal:</span>
            <span class="analysis-value signal-${data.combined_signal.action.toLowerCase()}">
                ${data.combined_signal.action} (${(data.combined_signal.confidence * 100).toFixed(0)}%)
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Market Sentiment:</span>
            <span class="analysis-value">${data.market_sentiment.overall_sentiment}</span>
        </div>
    `;
    
    container.innerHTML = html;
}

// Update performance metrics
function updatePerformanceMetrics(performance) {
    document.getElementById('currentCapital').textContent = 
        `$${performance.current_capital.toFixed(2)}`;
    
    const returnEl = document.getElementById('totalReturn');
    const returnClass = performance.total_return >= 0 ? 'positive' : 'negative';
    returnEl.className = `metric-value ${returnClass}`;
    returnEl.textContent = 
        `$${performance.total_return.toFixed(2)} (${performance.total_return_pct.toFixed(2)}%)`;
    
    document.getElementById('totalTrades').textContent = performance.total_trades;
    document.getElementById('winRate').textContent = `${performance.win_rate.toFixed(2)}%`;
}

// Update current position
function updateCurrentPosition(position) {
    const container = document.getElementById('currentPosition');
    
    if (!position) {
        container.innerHTML = '<p class="no-data">No open position</p>';
        return;
    }
    
    const html = `
        <div class="position-item">
            <span class="analysis-label">Side:</span>
            <span class="analysis-value">${position.side.toUpperCase()}</span>
        </div>
        <div class="position-item">
            <span class="analysis-label">Amount:</span>
            <span class="analysis-value">${position.amount.toFixed(4)}</span>
        </div>
        <div class="position-item">
            <span class="analysis-label">Entry Price:</span>
            <span class="analysis-value">$${position.entry_price.toFixed(2)}</span>
        </div>
        <div class="position-item">
            <span class="analysis-label">Stop Loss:</span>
            <span class="analysis-value">$${position.stop_loss.toFixed(2)}</span>
        </div>
        <div class="position-item">
            <span class="analysis-label">Take Profit:</span>
            <span class="analysis-value">$${position.take_profit.toFixed(2)}</span>
        </div>
    `;
    
    container.innerHTML = html;
}

// Update recent trades
function updateRecentTrades(trades) {
    const container = document.getElementById('recentTrades');
    
    if (!trades || trades.length === 0) {
        container.innerHTML = '<p class="no-data">No trades yet</p>';
        return;
    }
    
    const html = trades.reverse().map(trade => {
        const tradeClass = trade.pnl >= 0 ? 'profit' : 'loss';
        const actionIcon = trade.action === 'OPEN' ? '🔵' : '⚪';
        
        return `
            <div class="trade-item ${tradeClass}">
                <div class="trade-header">
                    <span>${actionIcon} ${trade.action} ${trade.side || ''}</span>
                    <span>${new Date(trade.timestamp).toLocaleString()}</span>
                </div>
                <div class="trade-details">
                    Price: $${trade.price ? trade.price.toFixed(2) : trade.exit_price.toFixed(2)} | 
                    Amount: ${trade.amount.toFixed(4)}
                    ${trade.pnl ? ` | PnL: $${trade.pnl.toFixed(2)} (${trade.pnl_pct.toFixed(2)}%)` : ''}
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

// Update chart
function updateChart(chartData) {
    if (!chartData || !priceChart) return;
    
    const labels = chartData.timestamps.map(ts => {
        const date = new Date(ts);
        return date.toLocaleTimeString();
    });
    
    priceChart.data.labels = labels.slice(-50);
    priceChart.data.datasets[0].data = chartData.prices.slice(-50);
    priceChart.update();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeChart();
    logMessage('Dashboard loaded. Initialize the bot to begin.', 'info');
    updateStatus('inactive', 'Not Initialized');
});
