document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const resultContainer = document.getElementById('result-container');
    const resultIcon = document.getElementById('result-icon');
    const resultText = document.getElementById('result-text');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get values
        const income = document.getElementById('income').value;
        const creditScore = document.getElementById('credit_score').value;
        const employmentStatus = document.getElementById('employment_status').value;
        const loanAmount = document.getElementById('loan_amount').value;

        // Validation
        if (!income || !creditScore || !employmentStatus || !loanAmount) {
            alert('Please fill out all fields.');
            return;
        }

        // UI State: Loading
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        // Hide previous result
        if (!resultContainer.classList.contains('hidden')) {
            resultContainer.classList.add('hidden');
        }

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    income: income,
                    credit_score: creditScore,
                    employment_status: employmentStatus,
                    loan_amount: loanAmount
                })
            });

            const data = await response.json();

            // Fake delay for UX (showing the loading spinner)
            setTimeout(() => {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;

                if (response.ok) {
                    showResult(data.prediction);
                } else {
                    alert(data.error || 'Something went wrong.');
                }
            }, 800);

        } catch (error) {
            console.error('Error:', error);
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            alert('Failed to connect to the server. Is it running?');
        }
    });

    function showResult(prediction) {
        resultContainer.classList.remove('hidden');
        
        // Reset classes
        resultText.className = 'result-text';
        
        if (prediction === 'Approved') {
            resultIcon.innerHTML = '🎉';
            resultText.innerText = 'Loan Approved!';
            resultText.classList.add('result-approved');
        } else {
            resultIcon.innerHTML = '🛑';
            resultText.innerText = 'Loan Rejected';
            resultText.classList.add('result-rejected');
        }
    }
});
