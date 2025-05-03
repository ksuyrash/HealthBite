document.addEventListener("DOMContentLoaded", function () {
  console.log("main.js loaded");

  // BMI Calculator
  document.getElementById("bmi-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const height = parseFloat(document.getElementById("bmi-height").value);
    const weight = parseFloat(document.getElementById("bmi-weight").value);
    const bmi = weight / (height / 100) ** 2;

    let category = "";
    if (bmi < 18.5) category = "Underweight";
    else if (bmi < 25) category = "Healthy weight";
    else if (bmi < 30) category = "Overweight";
    else category = "Obese";

    document.getElementById(
      "bmi-result"
    ).textContent = `Your BMI is ${bmi.toFixed(2)} (${category})`;
  });

  // Calorie Needs + Goal Handling
  document
    .getElementById("calorie-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();

      const age = parseFloat(document.getElementById("age").value);
      const gender = document.getElementById("gender").value;
      const height = parseFloat(document.getElementById("cal-height").value);
      const weight = parseFloat(document.getElementById("cal-weight").value);
      const activity = parseFloat(document.getElementById("activity").value);
      const goalWeightInput = document.getElementById("goal-weight").value;
      const intensity = parseFloat(document.getElementById("intensity").value);

      let bmr;
      if (gender === "male") {
        bmr = 10 * weight + 6.25 * height - 5 * age + 5;
      } else {
        bmr = 10 * weight + 6.25 * height - 5 * age - 161;
      }

      const maintenanceCalories = bmr * activity;

      document.getElementById(
        "calorie-result"
      ).textContent = `You need approximately ${Math.round(
        maintenanceCalories
      )} calories/day to maintain your weight.`;

      // If goal weight provided, calculate surplus/deficit
      if (goalWeightInput) {
        const goalWeight = parseFloat(goalWeightInput);
        const weightDiff = goalWeight - weight;

        if (weightDiff === 0) {
          document.getElementById("goal-result").textContent =
            "You're already at your goal weight.";
          return;
        }

        const totalCalorieChange = weightDiff * 7700; // 7700 kcal per 1kg fat
        const daysNeeded = Math.ceil(Math.abs(totalCalorieChange / intensity));
        const dailyCalories =
          maintenanceCalories + (weightDiff > 0 ? intensity : -intensity);

        document.getElementById(
          "goal-result"
        ).textContent = `To reach your goal of ${goalWeight} kg, eat about ${Math.round(
          dailyCalories
        )} kcal/day.
        Estimated time: ${daysNeeded} days (${(daysNeeded / 7).toFixed(
          1
        )} weeks).`;
      } else {
        document.getElementById("goal-result").textContent = "";
      }
    });
});
