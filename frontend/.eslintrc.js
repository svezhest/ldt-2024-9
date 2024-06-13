// eslint-disable-next-line no-undef
module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:prettier/recommended',
    'prettier',
    'plugin:react/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  plugins: ['react', '@typescript-eslint', 'prettier', 'react-hooks'],
  rules: {
    'no-console': 'error',
    'no-debugger': 'error',
    'import/default': ['off'],

    // Typescript
    '@typescript-eslint/no-non-null-assertion': 'error',
    eqeqeq: ['error', 'always', {null: 'ignore'}],
    '@typescript-eslint/no-empty-interface': ['error', {allowSingleExtends: true}],
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        ignoreRestSiblings: true,
        argsIgnorePattern: '^_',
        args: 'after-used',
      },
    ],
    '@typescript-eslint/ban-types': ['warn'],
    '@typescript-eslint/no-empty-function': ['warn'],
    '@typescript-eslint/no-non-null-asserted-optional-chain': ['warn'],

    // JSX
    'react/jsx-curly-brace-presence': ['error', 'never'],
    'react/jsx-boolean-value': ['error', 'never'],
    'react/jsx-no-target-blank': ['off'],
    'react/react-in-jsx-scope': ['off'],
    'react/prop-types': ['off'],

    // General
    'no-prototype-builtins': ['off'],
    curly: ['error'],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
}
