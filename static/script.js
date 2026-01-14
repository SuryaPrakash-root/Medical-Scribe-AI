document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const transcriptInput = document.getElementById('transcriptInput');
    const soapContainer = document.getElementById('soapContainer');
    const placeholder = document.getElementById('placeholder');
    const btnText = document.getElementById('btnText');
    const loadingSpinner = document.getElementById('loadingSpinner');

    generateBtn.addEventListener('click', async () => {
        const transcript = transcriptInput.value.trim();
        if (!transcript) {
            alert('Please enter a conversation transcript.');
            return;
        }

        // Set loading state
        setLoading(true);
        soapContainer.style.display = 'none';
        placeholder.style.display = 'none';

        try {
            const response = await fetch('/generate-soap', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcript }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate SOAP note');
            }

            const data = await response.json();
            renderSOAP(data);

        } catch (error) {
            console.error('Error:', error);
            alert('Error generating SOAP note: ' + error.message);
            placeholder.style.display = 'flex';
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            generateBtn.disabled = true;
            btnText.textContent = 'Generating...';
            loadingSpinner.style.display = 'inline-block';
        } else {
            generateBtn.disabled = false;
            btnText.textContent = 'Generate SOAP Note';
            loadingSpinner.style.display = 'none';
        }
    }

    function renderSOAP(data) {
        if (data.status === 'insufficient_clinical_data') {
            soapContainer.innerHTML = `
                <div class="visit-summary" style="background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.2); color: #fca5a5;">
                    <h3>Insufficient Clinical Data</h3>
                    <p>The transcript provided does not contain enough clinical information to generate a SOAP note.</p>
                </div>
            `;
        } else {
            // Helper to render lists
            const renderList = (items) => {
                if (!items || items.length === 0) return '<p>None</p>';
                return `<ul class="soap-list">${items.map(item => `<li>${item}</li>`).join('')}</ul>`;
            };

            // Helper to render key-value pairs if object
            const renderDict = (obj) => {
                if (!obj) return '';
                return Object.entries(obj).map(([key, value]) =>
                    `<div style="margin-bottom: 0.5rem;">
                        <span style="color: var(--text-secondary); text-transform: capitalize;">${key.replace(/_/g, ' ')}:</span> 
                        <span style="color: var(--text-primary);">${value || 'N/A'}</span>
                    </div>`
                ).join('');
            };

            soapContainer.innerHTML = `
                <div class="visit-summary">
                    <h3>Visit Summary</h3>
                    <p>${data.visit_summary}</p>
                </div>

                <div class="soap-card subjective">
                    <h3>Subjective (S)</h3>
                    <div class="soap-content">
                        <div style="margin-bottom: 0.5rem;"><strong style="color: #f472b6;">Chief Complaint:</strong> ${data.subjective.chief_complaint}</div>
                        <div><strong style="color: #f472b6;">HPI:</strong> ${data.subjective.hpi}</div>
                    </div>
                </div>

                <div class="soap-card objective">
                    <h3>Objective (O)</h3>
                    <div class="soap-content">
                         ${renderDict(data.objective)}
                    </div>
                </div>

                <div class="soap-card assessment">
                    <h3>Assessment (A)</h3>
                    <div class="soap-content">
                        ${renderList(data.assessment)}
                    </div>
                </div>

                <div class="soap-card plan">
                    <h3>Plan (P)</h3>
                    <div class="soap-content">
                        <div style="margin-bottom: 0.5rem;"><strong style="color: #4ade80;">Medications:</strong> ${renderList(data.plan.medications)}</div>
                        <div style="margin-bottom: 0.5rem;"><strong style="color: #4ade80;">Labs Ordered:</strong> ${renderList(data.plan.labs)}</div>
                        <div style="margin-bottom: 0.5rem;"><strong style="color: #4ade80;">Referrals:</strong> ${renderList(data.plan.referrals)}</div>
                        <div style="margin-bottom: 0.5rem;"><strong style="color: #4ade80;">Instructions:</strong> ${renderList(data.plan.instructions)}</div>
                        <div><strong style="color: #4ade80;">Follow Up:</strong> ${data.plan.follow_up}</div>
                    </div>
                </div>
            `;
        }

        soapContainer.style.display = 'flex';
    }
});
