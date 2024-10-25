async function showAddMenuModal() {
    document.querySelector("#modal").classList.remove("hidden");
  
    document.getElementById("confirm-modal").onclick = async function () {
        await addMenu();
        closeModal();
    };
  }
  
  function closeModal() {
    document.querySelector("#form").reset();
    window.location.href="/explore";
    document.querySelector("#modal").classList.add("hidden");
  }
  
  async function addMenu() {
    const form = new FormData(document.querySelector("#form"));
    const response = await fetch("/explore/add_menu/", {
      method: "POST",
      body: form,
    });
  
    if (!response.ok) {
      throw new Error("Failed to add menu");
    }
    return false;
  }

  function submitFilterForm() {
    var form = document.getElementById('filterForm');
    form.reset();
 
    form.submit();
  }
  
  function returnToList(){
    window.location.href="/explore";
  }

  function toggleFilter() {
    const filterOptions = document.getElementById("filter-options");
    if (filterOptions.classList.contains("hidden")) {
        filterOptions.classList.remove("hidden");
    } else {
        filterOptions.classList.add("hidden");
    }
}
  
  document.getElementById("cancel-modal").addEventListener("click", closeModal);
  