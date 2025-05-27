const form = document.getElementById('imageForm');
const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const result = document.getElementById('result');

imageInput.onchange = () => {
    const file = imageInput.files[0];
    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
    }
};

form.onsubmit = async (e) => {
    e.preventDefault();
    const file = imageInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    result.textContent = "Analyzing...";

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        // Try to parse the body regardless of success or failure
        const contentType = response.headers.get("content-type");

        let data;
        if (contentType && contentType.includes("application/json")) {
            data = await response.json();
        } else {
            data = await response.text();
        }

        if (response.ok) {
    const message = `Result: ${data.result || JSON.stringify(data)}`;
    result.textContent = message;
    alert(message);
}

        else {
            const errorMsg = `Server error (${response.status}): ${JSON.stringify(data)}`;
            result.textContent = errorMsg;
            alert(errorMsg);
        }
    } catch (error) {
        const errorMsg = `Network error: ${error.message}`;
        result.textContent = errorMsg;
        alert(errorMsg);
        console.error(error);
    }
};
