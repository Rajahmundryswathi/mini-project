// Function to handle search by query
function searchBooks() {
    const query = document.getElementById('searchQuery').value;
    console.log(`Searching for: ${query}`);  // Debug statement

    fetch(`http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);  // Debug statement
            displayResults(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Function to handle search by rack
function searchByRack() {
    const rackNumber = document.getElementById('rackDropdown').value;
    if (rackNumber) {
        fetch(`http://127.0.0.1:5000/search?rack=${encodeURIComponent(rackNumber)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Data received:', data);  // Debug statement
                displayResults(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }
}

// Function to display search results
function displayResults(data) {
    const resultContainer = document.getElementById('resultContainer');
    resultContainer.innerHTML = ''; // Clear previous results

    if (data.total_results === 0) {
        resultContainer.innerHTML = '<p>No books found matching your query.</p>';
    } else {
        data.books.forEach(book => {
            const bookElement = document.createElement('div');
            bookElement.classList.add('book');
            bookElement.innerHTML = `
                <h2>${book.title}</h2>
                <p><strong>Author:</strong> ${book.author}</p>
                <p><strong>Description:</strong> ${book.description}</p>
                <p><strong>Keywords:</strong> ${book.keywords}</p>
            `;
            resultContainer.appendChild(bookElement);
        });
    }
}
