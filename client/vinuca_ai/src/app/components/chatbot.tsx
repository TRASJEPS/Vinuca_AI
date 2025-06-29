// components/Chat.tsx
"use client"; // This ensures the component runs on the client side.

import { useState, Suspense } from "react";

export default function Chat() {
  const [query, setQuery] = useState(""); // Stores user input
  const [response, setResponse] = useState(""); // Stores AI response
  const [products, setProducts] = useState([]); // ADDED: Stores parsed product data
  const [loading, setLoading] = useState(false); // Tracks loading state

  // ADDED: Function to parse product data from streaming response
  function parseProductsFromResponse(responseText) {
    const products = [];
    
    // UPDATED: Parse your specific response format with numbered products
    // Look for pattern: 1. **Product Name** followed by * Price: and * Product Link:
    // const productPattern = /(\d+)\.\s*\*\*([^*]+)\*\*\s*\*\s*Price:\s*([^\n*]+)\s*\*\s*Top Active Ingredients:\s*([^\n*]+)\s*\*\s*Product Link:\s*\[([^\]]+)\]\(([^)]+)\)/g;
    // const productPattern = /(\d+)\.\s*\*\*([^*]+)\*\*\s*\*\s*Price:\s*([^\n*]+)\s*\*\s*Top Active Ingredients:\s*([^\n*]+)\s*\*\s*Product Link:\s*\[([^\]]+)\]\(([^)]+)\)/g;

    // 6/28/25 Added: Regex for alternate format (angle brackets for links, no markdown link)
    // const productPattern = /(\d+)\.\s*\*\*([^*]+)\*\*:?\s*\*?\s*\*?Price:?\*?\s*([\$\d.,\-\s]+)\*?\s*\*?Top Active Ingredients:?\*?\s*([^*\n]+)\*?\s*\*?Product Link:?\*?\s*<([^>]+)>/g;

    // 6/29/25 Added: Regex for format with Brand Name field
    //const productPattern = /(\d+)\.\s*\*\*([^*]+)\*\*\s*Brand Name:\s*([^\n*]+)\s*\*?\s*Price:?:?\*?\s*([\$\d.,\-\s]+)\*?\s*\*?Top Active Ingredients:?:?\*?\s*([^*\n]+)\*?\s*\*?Product Link:?:?\*?\s*<([^>]+)>/g;

    // 6/29/25 updated with new prompt format with labeled fields
    const productPattern = /(\d+)\.\s*\*\*([^\*]+)\*\*\s*Brand Name:\s*([^\n]+)\s*Price:\s*([^\n]+)\s*Top Active Ingredients:\s*([^\n]+)\s*Product Link:\s*<?([^\s>]+)>?/g;

//  let match;
//     while ((match = productPattern.exec(responseText)) !== null) {
//       products.push({
//         product_name: match[2].trim(),
//         //brand_name: match[2].trim(),
//         price: match[3].trim(),
//         // details: `Recommended for your hair concerns`, // Since details aren't in your format
//         ingredients: match[4].trim(),
//         product_link: match[6].trim() // The actual URL from markdown link
//       });
//     }


// MAKE SURE THIS REGEX MATCHES YOUR FORMAT FOR EACH MATCHING GROUP
    let match;
    while ((match = productPattern.exec(responseText)) !== null) {
      products.push({
        product_name: match[2].trim(),
        brand_name: match[3].trim(),
        price: match[4].trim(),
        // details: `Recommended for your hair concerns`, // Since details aren't in your format
        ingredients: match[5].trim(),
        product_link: match[6].trim() // The actual URL from markdown link
      });
    }
    
    // If the above doesn't work, try a simpler approach
    if (products.length === 0) {
      // Split by numbered items and parse each
      const numberedSections = responseText.split(/\d+\.\s*\*\*/);
      
      for (let i = 1; i < numberedSections.length; i++) {
        const section = numberedSections[i];
        
        // Extract product name (everything before the first *)
        const nameMatch = section.match(/^([^*]+)/);
        const brandMatch = section.match(/^([^*]+)/);
        const priceMatch = section.match(/\*\s*Price:\s*([^\n*]+)/);
        const ingredientsMatch = section.match(/\*\s*Top Active Ingredients:\s*([^\n*]+)/);
        const linkMatch = section.match(/\*\s*Product Link:\s*\[([^\]]+)\]\(([^)]+)\)/);
        
        if (nameMatch && priceMatch && linkMatch) {
          products.push({
            product_name: nameMatch[1].trim(),
            brand_name: brandMatch[1].trim(),
            price: priceMatch[1].trim(),
            // details: `Perfect for addressing your hair concerns`, // Not yet format later
            ingredients: ingredientsMatch ? ingredientsMatch[1].trim() : 'See product page for full ingredients',
            product_link: linkMatch[2].trim()
          });
        }
      }
    }
    
    return products;
  }

  // ADDED: Function to check if response contains product data
  function hasProductData(responseText) {
    // UPDATED: Check for your specific product format indicators
    const productIndicators = [
      /\d+\.\s*\*\*.*\*\*/,  // Numbered items with bold product names
      'Brand Name:',
      'Price:',
      'Top Active Ingredients:',
      'Product Link:'
    ];
    
    return productIndicators.some(indicator => {
      if (indicator instanceof RegExp) {
        return indicator.test(responseText);
      }
      return responseText.includes(indicator);
    });
  }

  // MODIFIED: Function to stream output from AI with product parsing
  async function sendMessage() {
    if(!query.trim()) return;

    setLoading(true);
    setResponse('');
    setProducts([]); // ADDED: Clear previous products

    try {
      const res = await fetch("http://localhost:8000/api/gemini-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query, chat_history: []}), // Send user input as JSON
      });

      // check if response status okay and if data is returned
      if (!res.ok || !res.body) throw new Error("Gemini response stream failed");

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
   
      let done = false;
      let fullResponse = ''; // ADDED: Track full response for parsing
   
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunk = decoder.decode(value);
        
        if (chunk) {
          fullResponse += chunk; // ADDED: Build full response
          setResponse(fullResponse); // Update display with full response
        }
        console.log(chunk);
      }
      
      // ADDED: After streaming is complete, check for products
      if (hasProductData(fullResponse)) {
        const parsedProducts = parseProductsFromResponse(fullResponse);
        if (parsedProducts.length > 0) {
          setProducts(parsedProducts);
        }
      }
      
    } catch (err) {
      console.error("Streaming error:", err);
      setResponse("STREAMING ERROR.");
    } finally {
      setLoading(false);
    }
  }

  // ADDED: Component to display individual product cards
  const ProductCard = ({ product, index }) => (
    <div className="bg-white border border-gray-200 rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-bold text-gray-800 mb-2">{product.product_name}</h3>
      <h3 className="text-lg font-bold text-gray-800 mb-2">{product.brand_name}</h3>
      
      <div className="mb-3">
        <span className="text-xl font-semibold border-gray-200 rounded-lg p-2 bg-[rgb(194,228,255)] text-black-600">{product.price}</span>
      </div>
      
      {/* <div className="mb-3">
        <p className="text-gray-600 text-sm leading-relaxed">{product.details}</p>
      </div> */}

      <div className="mb-4">
        <h4 className="font-semibold text-gray-700 mb-1 text-sm">Active Ingredients:</h4>
        <p className="text-gray-600 text-xs leading-relaxed">{product.ingredients}</p>
      </div>

      {product.product_link && (
        <div className="mt-4">
          <a 
            href={product.product_link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-block bg-[rgb(255,149,202)] hover:bg-pink-600 text-white px-3 py-2 rounded text-sm font-medium transition-colors w-full text-center"
          >
            View Product →
          </a>
        </div>
      )}
    </div>
  );

  // MODIFIED: Updated return statement with conditional rendering
  return (
    <div className="p-8 max-w-9/10 mx-auto bg-white rounded-lg shadow-md">
      <h2 className="text-xl p-4 font-semibold mb-2 text-center">Your Virtual Beauty Assistant</h2>
      
      {/* MODIFIED: Conditional rendering based on whether products are found */}
      {response && (
        <div className="mb-6">
          <div className="flex p-2 mb-4 bg-gray-100 border rounded">
            <img src="../favicon.ico" alt="Description" className="w-6 h-6 mr-2" />
            <strong className="pr-2">Vinuca:</strong> 
            {/* MODIFIED: Show different message based on product presence */}
            {products.length > 0 ? (
              <span>Here are my recommendations for you:</span>
            ) : (
              <span>{response}</span>
            )}
          </div>
          
          {/* ADDED: Product cards display - 3 cards per row with 33% width each */}
          {products.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {products.map((product, index) => (
                <ProductCard key={index} product={product} index={index} />
              ))}
            </div>
          )}
        </div>
      )}

      <div className="flex gap-4 align-middle items-center border rounded">
        <textarea
          className="w-full p-4 resize-none"
          placeholder="How can I help you?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={1}
        ></textarea>

        <button
          className={`px-4 py-2 mr-2 ${loading ? 'bg-[rgb(0,0,255)]' : 'bg-[rgb(255,149,202)]'} text-white font-bold rounded disabled:opacity-50 hover:bg-[rgb(255,110,199)]`}
          onClick={sendMessage}
          disabled={loading}
        >
          {loading ? ( 
            <>
            <svg className="size-5 animate-spin ..." viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            </>
            ) 
          : "⤴"}
        </button>
      </div>
    </div>
  );
}