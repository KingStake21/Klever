let validator = {
    address: "klv17xeym2mn5lrswvu6kkus6jq2k3kkn3keh3zterr3h97l68tqtzdsggksdg",
    logo: "https://raw.githubusercontent.com/KingStake21/Klever/main/Kube1.png",
    fetchValidator: function () {
      fetch(
        "https://api.mainnet.klever.finance/v1.0/validator/" + this.address
      )
        .then((response) => {
          if (!response.ok) {
            alert("No Validator Found.");
            throw new Error("No Validator Found.");
          }
          return response.json();
        })
        .then((info) => this.displayValidator(info.data.validator))
        .catch((error) => console.error(error)); // Handle errors
    },
    displayValidator: function (validatorData) {
      if (!validatorData) {
        console.error("Invalid API response structure");
        return;
      }
  
      const { name, list, totalStake, maxDelegation, tempRating, commission} = validatorData;
      const freeSpace = maxDelegation - totalStake;
      const listElement = document.querySelector(".list");
  
      document.querySelector(".ticker").innerHTML = name;
      document.querySelector(".logo").src = this.logo;
      document.querySelector(".list").innerHTML = `<span class="text">Status:</span> ${list}`;
      document.querySelector(".maxDelegation").innerHTML = `<span class="text">Max:</span> ${(totalStake / 1000000).toLocaleString('en-US', { maximumFractionDigits: 2 })} KLV`;
      document.querySelector(".totalStake").innerHTML = `<span class="text">Total:</span> ${(maxDelegation / 1000000).toLocaleString('en-US', { maximumFractionDigits: 2 })} KLV`;
      document.querySelector(".freeSpace").innerHTML = `<span class="text">Free:</span> ${(freeSpace / 1000000).toLocaleString('en-US', { maximumFractionDigits: 2 })} KLV`;
      document.querySelector(".tempRating").innerHTML = `<span class="text">Rating:</span> ${(tempRating/100000).toLocaleString('en-US', { maximumFractionDigits: 2 })} %`;
      document.querySelector(".commission").innerHTML = `<span class="text">Commission:</span> ${(commission/100).toLocaleString('en-US', { maximumFractionDigits: 2 })} %`;
      document.querySelector(".validator").classList.remove("loading");
      
      // Set color based on the value of 'list'
    switch (list.toLowerCase()) {
        case "elected":
            listElement.style.color = "green";
        break;
        case "eligible":
            listElement.style.color = "orange";
        break;
        case "waiting":
            listElement.style.color = "yellow";
        break;
        case "jailed":
            listElement.style.color = "red";
        break;
        default:
            listElement.style.color = "black"; // Default color
    }
  
  // Update the text content
  listElement.innerText = "Status: " + list;
    },
  };
  
  // Example usage:
  validator.fetchValidator();
  