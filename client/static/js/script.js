// const form = document.getElementById('imageForm');
// const imageInput = document.getElementById('imageInput');
// const preview = document.getElementById('preview');
// const result = document.getElementById('result');

// imageInput.onchange = () => {
//     const file = imageInput.files[0];
//     if (file) {
//         preview.src = URL.createObjectURL(file);
//         preview.style.display = 'block';
//     }
// };

// form.onsubmit = async (e) => {
//     e.preventDefault();
//     const file = imageInput.files[0];
//     const formData = new FormData();
//     formData.append('image', file);

//     result.textContent = "Analyzing...";

//     try {
//         const response = await fetch('/analyze', {
//             method: 'POST',
//             body: formData
//         });

//         // Try to parse the body regardless of success or failure
//         const contentType = response.headers.get("content-type");

//         let data;
//         if (contentType && contentType.includes("application/json")) {
//             data = await response.json();
//         } else {
//             data = await response.text();
//         }

//         if (response.ok) {
//     const message = `📊Result: ${data.result || JSON.stringify(data)}`;
//     result.textContent = message;
//     alert(message);
// }

//         else {
//             const errorMsg = `Server error (${response.status}): ${JSON.stringify(data)}`;
//             result.textContent = errorMsg;
//             alert(errorMsg);
//         }
//     } catch (error) {
//         const errorMsg = `Network error: ${error.message}`;
//         result.textContent = errorMsg;
//         alert(errorMsg);
//         console.error(error);
//     }
// };
// DOM elements
        const form = document.getElementById('imageForm');
        const imageInput = document.getElementById('imageInput');
        const uploadArea = document.getElementById('uploadArea');
        const preview = document.getElementById('preview');
        const previewContainer = document.getElementById('previewContainer');
        const analyzeButton = document.getElementById('analyzeButton');
        const resultsSection = document.getElementById('resultsSection');
        const resultIcon = document.getElementById('resultIcon');
        const resultTitle = document.getElementById('resultTitle');
        const resultText = document.getElementById('resultText');
        const confidenceFill = document.getElementById('confidenceFill');
        const confidenceText = document.getElementById('confidenceText');
        const classificationValue = document.getElementById('classificationValue');
        const confidenceValue = document.getElementById('confidenceValue');
        const rawPredictionValue = document.getElementById('rawPredictionValue');
        const processingTimeValue = document.getElementById('processingTimeValue');

        let startTime;

        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                imageInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        // File input change handler
        imageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                handleFileSelect(file);
            }
        });

        // Handle file selection
        function handleFileSelect(file) {
            // Validate file size
            if (file.size > 16 * 1024 * 1024) {
                showError('File size must be less than 16MB');
                return;
            }

            // Validate file type
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/bmp'];
            if (!allowedTypes.includes(file.type)) {
                showError('Please select a valid image file (JPG, PNG, GIF, WebP, BMP)');
                return;
            }

            // Show preview
            preview.src = URL.createObjectURL(file);
            previewContainer.classList.add('show');
            
            // Hide previous results
            resultsSection.classList.remove('show');
        }

        // Form submission handler
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const file = imageInput.files[0];
            if (!file) {
                showError('Please select an image file');
                return;
            }

            startTime = Date.now();
            setLoadingState(true);

            const formData = new FormData();
            formData.append('image', file);

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const contentType = response.headers.get("content-type");
                let data;

                if (contentType && contentType.includes("application/json")) {
                    data = await response.json();
                } else {
                    const text = await response.text();
                    data = { error: text };
                }

                if (response.ok && data.success) {
                    showResults(data);
                } else {
                    showError(data.error || `Server error (${response.status})`);
                }
            } catch (error) {
                showError(`Network error: ${error.message}`);
                console.error('Analysis error:', error);
            } finally {
                setLoadingState(false);
            }
        });

        // Set loading state
        function setLoadingState(loading) {
            analyzeButton.disabled = loading;
            const buttonContent = analyzeButton.querySelector('.button-content');
            
            if (loading) {
                buttonContent.innerHTML = `
                    <div class="spinner"></div>
                    <span>Analyzing...</span>
                `;
            } else {
                buttonContent.innerHTML = `
                    <i class="fas fa-microscope"></i>
                    <span>Analyze Image</span>
                `;
            }
        }

        // Show results
        function showResults(data) {
            const processingTime = Date.now() - startTime;
            const isAI = data.classification === 'ai';
            
            // Update result icon and title
            resultIcon.innerHTML = isAI ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
            resultIcon.style.color = isAI ? '#ff6b6b' : '#00d4aa';
            
            // Update result text
            resultText.innerHTML = `
                <div style="font-size: 1.25rem; margin-bottom: 1rem;">
                    ${isAI ? '🤖' : '🧠'} <strong>This image appears to be ${isAI ? 'AI-Generated' : 'Human-Created'}</strong>
                </div>
            `;

            // Update confidence meter
            confidenceFill.style.width = `${data.confidence}%`;
            confidenceText.textContent = `${data.confidence}% Confidence`;
            
            // Update detail cards
            classificationValue.textContent = isAI ? 'AI-Generated' : 'Human-Created';
            confidenceValue.textContent = `${data.confidence}%`;
            rawPredictionValue.textContent = data.raw_prediction.toFixed(4);
            processingTimeValue.textContent = `${processingTime}ms`;

            // Apply appropriate styling
            resultsSection.className = `results-section show ${isAI ? 'ai-result' : 'success'}`;
        }

        // Show error
        function showError(message) {
            resultIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
            resultTitle.textContent = 'Analysis Failed';
            resultText.innerHTML = `<div style="color: #ff6b6b;">${message}</div>`;
            
            // Reset other elements
            confidenceFill.style.width = '0%';
            confidenceText.textContent = '';
            classificationValue.textContent = '-';
            confidenceValue.textContent = '-';
            rawPredictionValue.textContent = '-';
            processingTimeValue.textContent = '-';

            resultsSection.className = 'results-section show error';
        }

        // Cleanup object URLs to prevent memory leaks
        window.addEventListener('beforeunload', () => {
            if (preview.src.startsWith('blob:')) {
                URL.revokeObjectURL(preview.src);
            }
        });