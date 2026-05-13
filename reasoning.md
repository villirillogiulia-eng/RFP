# Reasoning

This file is used to document the reasoning behind architectural decisions, complex logic, and other significant project choices.
# 1. The Reasoning: Problem & Objective Tree

## Problem Tree (The "Why")
- **Root Cause 1:** Rapidly shifting conflict frontlines in Mudug, Somalia.
- **Root Cause 2:** Physical insecurity prevents manual school inspections.
- **Core Problem:** EBI lacks real-time visibility into which schools are safe, damaged, or serving displaced populations.
- **Consequences:** Misallocation of resources and children losing access to education.

## Objective Tree (The "How")
- **Technical Goal 1:** Use ACLED data to create a "Conflict Buffer Zone" (Risk Mapping).
- **Technical Goal 2:** Use HDX school coordinates to identify high-risk facilities.
- **Main Objective:** A dynamic decision-support tool that prioritizes schools based on safety and population shifts.
- **Expected Impact:** Improved education continuity and safer environments for students.