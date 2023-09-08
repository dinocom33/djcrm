/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/account/*.{html,js}',
        './templates/client/*.{html,js}',
        './templates/common/*.{html,js}',
        './templates/dashboard/*.{html,js}',
        './templates/lead/*.{html,js}',
        './templates/partials/*.{html,js}',
        './templates/profile/*.{html,js}',
        './templates/team/*.{html,js}',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}

