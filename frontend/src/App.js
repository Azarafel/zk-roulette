import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [backendStatus, setBackendStatus] = useState('Проверка...');
  const [betResult, setBetResult] = useState(null);

  // Проверка backend при загрузке
  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        const data = await response.json();
        setBackendStatus(`✅ Backend работает! Версия: ${data.version}`);
      } else {
        setBackendStatus('❌ Backend недоступен');
      }
    } catch (error) {
      setBackendStatus('❌ Ошибка подключения к backend');
    }
  };

  const testBet = async () => {
    try {
      const response = await fetch('http://localhost:8000/bet/prepare', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          number: 7,
          amount: 0.1,
          player_address: '0x1234567890123456789012345678901234567890'
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setBetResult('✅ Ставка подготовлена! ZK-proof сгенерирован');
      } else {
        setBetResult('❌ Ошибка при подготовке ставки');
      }
    } catch (error) {
      setBetResult('❌ Ошибка подключения к API');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎰 ZK-Roulette v2.0</h1>
        <p>Блокчейн рулетка с Zero-Knowledge Proof</p>
        
        <div className="status-panel">
          <h2>Статус системы:</h2>
          <p>{backendStatus}</p>
          <button onClick={checkBackend}>Обновить статус</button>
        </div>

        <div className="test-panel">
          <h2>Тест API:</h2>
          <button onClick={testBet}>Тест ставки (число 7, 0.1 ETH)</button>
          {betResult && <p>{betResult}</p>}
        </div>

        <div className="info-panel">
          <h2>🔥 Особенности:</h2>
          <ul>
            <li>🔒 Zero-Knowledge Proof - Приватные ставки</li>
            <li>🤖 ИИ-анализ - Детекция мошенничества</li>
            <li>⚡ Real-time - Мгновенная аналитика</li>
            <li>🛡️ Безопасность - Многоуровневая защита</li>
          </ul>
        </div>

        <div className="links-panel">
          <h2>📚 Полезные ссылки:</h2>
          <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
            📖 API Документация
          </a>
          <br />
          <a href="http://localhost:8000/health" target="_blank" rel="noopener noreferrer">
            ❤️ Health Check
          </a>
        </div>
      </header>
    </div>
  );
}

export default App; 