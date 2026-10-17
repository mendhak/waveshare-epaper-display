/**
* C-TOGGLE
* v0.3.1
* Toggle management
* https://github.com/ita-design-system/c-toggle.js
*/
const cToggle = {
    // Toggle methods enums
    methods: {
        add: 'add',
        remove: 'remove',
        toggle: 'toggle'
    },
    // Toggle ids that need to be closed when user clicks on document excepting on triggers nor targets
    // Array is populated on update method invoke
    dismissableIds: [],
    /**
     * DOCUMENT CLICK
     * @param {event} event handler method on document click
     */
    documentClick: function(event) {
        // Potential toggle target or trigger as ancestor
        const el_closest_toggle = event.target.closest('[c-toggle], [c-toggle-name]');
        if (el_closest_toggle === null) {
            // Click is anywhere but in a toggle trigger nor a target
            cToggle.dismissableIds.forEach(function(toggle_id) {
                cToggle.close(toggle_id);
            });
        } else {
            // Special case: user sets ids to force close on dataset "data-onclick-force-dismiss-children-ids"
            const close_children_ids = el_closest_toggle.dataset.onclickForceDismissChildrenIds;
            if (close_children_ids !== undefined) {
                cToggle.dismissableIds.forEach(function(toggle_id) {
                    if (close_children_ids.indexOf(toggle_id) > -1) {
                        cToggle.close(toggle_id);
                    }
                });
            }
        }
    },
    /**
     * SUBJOB
     * Apply routine of toggle job
     * @param {Object} el DOM element
     * @param {String} method must be 'add', 'remove' or 'toggle'
     * @param {String} id id of the toggle 
     */
    subjob: function(el, method, id) {
        // Element must have its own opened state classes defined
        if (el.dataset.openedStateClass !== undefined) {
            if (method == cToggle.methods.toggle) {
                // If origin classes are different from current class list
                if (el.dataset.classOrigin != el.classList.toString()) {
                    // Retrieve and apply saved class origin
                    el.setAttribute('class', el.dataset.classOrigin);
                    cToggle.instances[id].opened = false;
                } else {
                    // Apply replacement classes
                    el.setAttribute('class', el.dataset.openedStateClass);
                    cToggle.instances[id].opened = true;
                }
            } else if (method == cToggle.methods.add) {
                // Apply replacement classes
                el.setAttribute('class', el.dataset.openedStateClass);
                cToggle.instances[id].opened = true;
            } else if (method == cToggle.methods.remove) {
                // Retrieve and apply saved class origin
                el.setAttribute('class', el.dataset.classOrigin);
                cToggle.instances[id].opened = false;
            }
        }
    },
    /**
     * JOB
     * Routine applied on each toggle invoke
     * @param {String} id id of the toggle 
     * @param {String} method method to apply
     */
    job: function(id, method) {
        if (typeof id == 'string' && method in cToggle.methods) {
            if (typeof cToggle.instances[id] == 'object') {
                // JOB FOR TRIGGERS
                cToggle.instances[id].triggers.forEach(function(el) {
                    cToggle.subjob(el, method, id);
                });
                // JOB FOR TARGETS
                cToggle.instances[id].targets.forEach(function(el) {
                    cToggle.subjob(el, method, id);
                });
            }
        }
    },
    /**
     * OPEN
     * Method to invoke to open a toggle
     * @param {String} id id of the toggle to open
     */
    open: function(id) {
        cToggle.job(id, cToggle.methods.add);
        // Create custom event
        const event = new CustomEvent(`cToggle_event`, { detail: {id: id, method: 'open'} });
        document.dispatchEvent(event);
    },
    /**
     * CLOSE
     * Method to invoke to close a toggle
     * @param {String} id id of the toggle to close
     */
    close: function(id) {
        cToggle.job(id, cToggle.methods.remove);
        // Create custom event
        const event = new CustomEvent(`cToggle_event`, { detail: {id: id, method: 'close'} });
        document.dispatchEvent(event);
    },
    /**
     * TOGGLE
     * Method closes the specified toggle if opened and closes it if opened
     * @param {String} id id of the toggle
     */
    toggle: function(id) {
        cToggle.job(id, cToggle.methods.toggle);
        // Create custom event
        const event = new CustomEvent(`cToggle_event`, { detail: {id: id, method: 'toggle'} });
        document.dispatchEvent(event);
    },
    // Object populated by update() method
    instances: {
        // TOGGLE_ID: {
        //     targets: [el, el, ...],
        //     triggers: [el, el, ...]
        // }
    },
    /**
     * UPDATE
     * Method to invoke on each page load or DOM change
     */
    update: function() {
        // Iterate each trigger
        document.querySelectorAll('[c-toggle]').forEach(function(el_trigger) {
            // Get the toggle id
            const toggle_id = el_trigger.getAttribute('c-toggle');
            // Array of all targets elements with this toggle_id
            const els_targets = document.querySelectorAll('[c-toggle-name="'+toggle_id+'"]');
            // On targets, save the original class attribute before any change
            els_targets.forEach(function(el_target) {
                const current_class_attribute = el_target.getAttribute('class') || '';
                // Save current class state
                if (el_target.dataset.classOrigin === undefined) el_target.dataset.classOrigin = current_class_attribute;
            });
            // Get user settings
            const event_name = el_trigger.dataset.event;
            const dismiss = el_trigger.dataset.dismiss;
            const current_class_attribute = el_trigger.getAttribute('class') || '';
            // Save current class state
            el_trigger.dataset.classOrigin = current_class_attribute;
            // If no opened state class attribute
            if (el_trigger.dataset.openedStateClass === undefined) {
                // Sets class origin
                el_trigger.dataset.openedStateClass = current_class_attribute;
            }
            // Work only if at least one target exists
            if (els_targets.length > 0) {
                // Add listeners based on data-method
                if (event_name !== undefined) {
                    // Type of listener
                    if (event_name == 'mousehover' || event_name == 'mouseover') {
                        el_trigger.addEventListener('mouseenter', cToggle.handlers.mouseenter);
                        el_trigger.addEventListener('mouseleave', cToggle.handlers.mouseleave);
                    }
                    else if (event_name == 'mouseenter') {
                        el_trigger.addEventListener('mouseenter', cToggle.handlers.mouseenter);
                    }
                }
                // Default method applied
                else  {
                    el_trigger.addEventListener('click', cToggle.handlers.click);
                }
                // Write/overwrite instance
                cToggle.instances[toggle_id] = {
                    triggers: document.querySelectorAll(`[c-toggle="${toggle_id}"]`),
                    targets: els_targets,
                    opened: false
                }
                // Dismissable triggers and targets
                // Toggles that need to be closed when user clicks outside toggles triggers and targets
                if (dismiss == 'true') {
                    cToggle.dismissableIds.push(toggle_id);
                }
            }
        });
        // Bind document click to enable dismiss feature
        document.addEventListener('click', cToggle.documentClick);
    },
    handlers: {
        // On click on a trigger, get id and toggle
        click: function(e) {
            const target_id = e.target.closest('[c-toggle]').getAttribute('c-toggle');
            cToggle.toggle(target_id);
        },
        // On mouse enter a trigger, get id and open
        mouseenter: function(e) {
            const target_id = e.target.closest('[c-toggle]').getAttribute('c-toggle');
            cToggle.open(target_id);
        },
        // On mouse leave a trigger, get id and close
        mouseleave: function(e) {
            const target_id = e.target.closest('[c-toggle]').getAttribute('c-toggle');
            cToggle.close(target_id);
        }
    }
}
cToggle.update();
