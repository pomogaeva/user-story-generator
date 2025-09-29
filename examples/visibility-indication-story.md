# [Visibility] Implement Item-Level Visibility Indication in Grid and Live Modes

### **FEATURE CONTEXT**

This feature introduces visibility indication on item level within elements that support item-based visibility settings. It addresses the need for users to quickly identify when items within an element have custom visibility configurations, providing clear visual feedback about visibility states at both parent element and individual item levels.

The feature will benefit content creators, editors, and administrators who work with dynamic content elements, helping them understand and manage visibility settings more efficiently across complex content structures.

---

### **ACCEPTANCE CRITERIA**

**Scenario 1: Case 1 - Parent Element + Child Items with Visibility Settings**
- **Given** a parent element has visibility settings applied AND some child items have unique visibility settings
- **When** viewing the element in Grid mode or Live mode
- **Then** an eye icon should appear on both the parent element level and affected item levels
- **And** the icons should clearly indicate deviation from default parent visibility settings

**Scenario 2: Case 1 - Element Level Tooltip**
- **Given** hovering over the eye icon on the parent element level
- **When** the mouse hovers over the element-level eye icon
- **Then** a tooltip should appear with the text: "This element has visibility settings applied"

**Scenario 3: Case 1 - Item Level Tooltip**
- **Given** hovering over the eye icon on an item level
- **When** the mouse hovers over the item-level eye icon
- **Then** a tooltip should appear with the text: "This item has visibility settings applied"

**Scenario 4: Case 2 - No Parent Settings, Only Child Items**
- **Given** no parent element visibility settings exist AND some child items have unique visibility settings
- **When** viewing the element in Grid mode or Live mode
- **Then** an eye icon should appear on the parent element level with 60% opacity by default
- **And** eye icons should appear on affected item levels with full opacity

**Scenario 5: Case 2 - Parent Level Hover with 60% Opacity**
- **Given** the parent element has no visibility settings but some items do
- **When** hovering over the parent-level eye icon (60% opacity)
- **Then** the icon should become fully opaque
- **And** a tooltip should appear with the text: "Some items have visibility settings applied"

**Scenario 6: Case 2 - Item Level Tooltip**
- **Given** hovering over an item-level eye icon
- **When** the mouse hovers over the item-level eye icon
- **Then** a tooltip should appear with the text: "This item has visibility settings applied"

**Scenario 7: Live Mode Settings Dialog**
- **Given** the user is in Live mode for either case scenario
- **When** accessing the visibility tab in the settings dialog on item level
- **Then** all labels (where applicable) should use "item" instead of "element"

---

### **DESIGN**

- Designs provided in Figma:
  - Case 1 Design: https://www.figma.com/design/kc7bgj1ziwLKl9NvWl5rcA/Visibilty?node-id=3350-69247&m=dev
  - Case 2 Design: https://www.figma.com/design/kc7bgj1ziwLKl9NvWl5rcA/Visibilty?node-id=3350-69248&m=dev
- Designs approved by UX team with comprehensive interaction testing.

#### **Design Components Reference**
- **Visibility Eye Icon**: Use the standard visibility eye icon from the design system
- **Tooltip Component**: Implement hover-triggered tooltip with proper positioning
- **Opacity States**: Support 60% default opacity transitioning to 100% on hover
- **Grid Mode Layout**: Ensure icons are properly positioned within grid item containers
- **Live Mode Integration**: Icons should integrate seamlessly with live editing interface

#### **Design System Integration**
- **Icon Styles**: Use "icon-visibility" design token for consistent iconography
- **Color Tokens**: Apply "neutral-600" for default state, "neutral-900" for hover states
- **Opacity Values**: Implement "opacity-60" for default state, "opacity-100" for hover
- **Typography Scale**: Use "caption-small" for tooltip text
- **Component States**: Include default, hover, and active states for all visibility indicators

---

### **FUNCTIONAL DETAILS**

- **Icon Positioning**: Eye icons should be positioned in the top-right corner of both element and item containers
- **Opacity Behavior**:
  - Case 1: Full opacity (100%) on both element and item levels
  - Case 2: 60% opacity on parent element level, 100% opacity on item levels
- **Tooltip Implementation**: Hover-triggered tooltips with 300ms delay to prevent accidental triggers
- **Grid Mode**: Icons should not interfere with existing grid layout and item interactions
- **Live Mode**: Icons should be visible during live editing and not interfere with the editing experience
- **Settings Dialog**: Mirror existing parent-level settings dialog but with "item" terminology throughout
- **Design-driven functionality**: Icon hover states follow design system "Interactive Icon" pattern with smooth opacity transitions

---

### **DEPENDENCIES**

- Visibility settings system for parent elements (existing functionality)
- Item-level visibility configuration system
- Tooltip component library integration
- Grid layout system for proper icon positioning
- Live mode editing interface integration

---

### **SPECIAL CASES / EDGE CASES / LIMITATIONS**

- **Mixed Visibility States**: Handle complex scenarios where some items inherit parent settings while others have unique configurations
- **Performance Considerations**: Ensure tooltip rendering doesn't impact performance with large numbers of items
- **Mobile Responsiveness**: Verify tooltip positioning and touch interactions work correctly on mobile devices
- **Screen Reader Accessibility**: Ensure icons have proper ARIA labels for accessibility compliance
- **Browser Compatibility**: Test opacity transitions across all supported browsers

---

### **ERROR HANDLING**

- N/A

---

### **TESTING & VALIDATION**

**QC Automation:**
- Automated tests for scenarios from both cases
- Performance tests for large numbers of items with visibility settings

**QC Manual:**
- Test both Case 1 and Case 2 scenarios in Grid and Live modes
- Verify tooltip text accuracy for all interaction states
- Test opacity transitions and hover behaviors
- Validate settings dialog functionality on item level with "item" terminology
- Test across different element types that support item visibility

**Design Review Needs** - UI/UX validation including:
- Design system compliance verification for visibility icon styles and opacity states
- Component usage validation against design specifications for tooltip positioning and behavior
- Interaction pattern testing against design prototypes for hover states and transitions
- Visual regression testing for design consistency across Grid and Live modes

**Content Needs** - Documentation updates for item-level visibility settings with usage examples and troubleshooting
