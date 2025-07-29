# Logos Theory Semantic Alignment Issue

## Executive Summary

While investigating requested comparison between default and logos theory counterfactual examples, a fundamental semantic discrepancy was discovered. After aligning the example sets, the logos theory produces **different logical results** than the default theory for identical counterfactual tests, indicating structural differences in the counterfactual operator implementations.

## Problem Analysis

### Background
The user requested comparison of counterfactual examples between:
- `/src/model_checker/theory_lib/default/examples/counterfactual.py`
- `/src/model_checker/theory_lib/logos/subtheories/counterfactual/examples.py`

### Initial Finding: Example Misalignment
The logos theory was testing completely different logical principles:

**Original Logos CF_CM_1:**
```
Premises: ['(A \\boxright B)']
Conclusions: ['(A \\rightarrow B)']
```

**Default Theory CF_CM_1:**
```
Premises: ['\\neg A', '(A \\boxright C)']
Conclusions: ['((A \\wedge B) \\boxright C)']
```

### Root Cause Discovery: Semantic Implementation Differences

After aligning examples, testing revealed **semantic behavior discrepancies**:

#### CF_CM_2 Test Case Analysis

**Default Theory Result:**
```
EXAMPLE CF_CM_2: there is a countermodel. 
Premises: ['\\neg A', '(A \\diamondright C)']
Premise 2: (A \diamondright C) = TRUE
Conclusion: ((A \\wedge B) \\diamondright C) = FALSE
Result: COUNTERMODEL FOUND (expected behavior)
```

**Logos Theory Result:**
```
EXAMPLE CF_CM_2: there is a countermodel. L
Premises: ['\\neg A', '(A \\diamondright C)']
Premise 2: (A \diamondright C) = FALSE  
Conclusion: ((A \\wedge B) \\diamondright C) = FALSE
Result: NO COUNTERMODEL (unexpected behavior)
```

**Critical Issue:** The logos theory evaluates `(A \\diamondright C)` as **FALSE** where the default theory evaluates it as **TRUE** for the same logical context.

## Technical Analysis

### Affected Components

1. **Counterfactual Operator Implementation**
   - File: `/src/model_checker/theory_lib/logos/subtheories/counterfactual/operators.py`
   - Class: `CounterfactualOperator` (line 23-107)
   - Semantic method: `true_at()`, `false_at()`, `extended_verify()`, `extended_falsify()`

2. **Might Counterfactual Operator Implementation**
   - File: `/src/model_checker/theory_lib/logos/subtheories/counterfactual/operators.py` 
   - Class: `MightCounterfactualOperator` (line 109-127)
   - Definition: Uses `CounterfactualOperator` as base, so inherits the semantic issues

3. **Semantic Foundation**
   - File: `/src/model_checker/theory_lib/logos/semantic.py`
   - Methods: `is_alternative()`, `max_compatible_part()`, `closer_world()`
   - Issue: `closer_world()` returns hardcoded `False` (line 363)

### Comparison Required

**Default Theory Counterfactual Operators:**
- File: `/src/model_checker/theory_lib/default/operators.py`
- Implementation: Uses bilateral truthmaker semantics
- Semantic basis: Standard hyperintensional framework

**Logos Theory Counterfactual Operators:**
- File: `/src/model_checker/theory_lib/logos/subtheories/counterfactual/operators.py`  
- Implementation: Uses alternative worlds and closeness relations
- Semantic basis: Modular hyperintensional framework with world similarity

### Key Semantic Differences Identified

1. **World Closeness Implementation**
   ```python
   # Logos implementation (problematic)
   def closer_world(self, world_u, world_v, eval_point):
       return z3.BoolVal(False)  # Placeholder returning False
   ```

2. **Alternative World Calculation**
   - Logos uses `is_alternative()` method for counterfactual worlds
   - Default theory may use different approach

3. **Verification Conditions**
   - Different `extended_verify()` and `extended_falsify()` implementations
   - May affect how counterfactual antecedents are evaluated

## Next Steps

### Phase 1: Comparative Analysis (High Priority)

1. **Compare Operator Implementations**
   ```bash
   # Compare counterfactual operator semantics
   diff /src/model_checker/theory_lib/default/operators.py \
        /src/model_checker/theory_lib/logos/subtheories/counterfactual/operators.py
   ```

2. **Analyze Default Theory Counterfactual Logic**
   - Read: `/src/model_checker/theory_lib/default/operators.py`
   - Identify: `CounterfactualOperator` and `MightCounterfactualOperator` classes
   - Document: Semantic clauses for `true_at()`, `false_at()`, verification methods

3. **Document Semantic Method Differences**
   - Create comparison table of key methods
   - Identify specific logical differences
   - Focus on: truth conditions, falsity conditions, world selection

### Phase 2: Implementation Alignment (High Priority)

1. **Fix World Closeness Logic**
   ```python
   # Replace placeholder in logos/semantic.py:363
   def closer_world(self, world_u, world_v, eval_point):
       # Implement proper similarity metric based on default theory
       pass
   ```

2. **Align Counterfactual Operator Semantics**
   - Update `CounterfactualOperator.true_at()` in logos theory
   - Update `CounterfactualOperator.false_at()` in logos theory
   - Ensure verification/falsification methods match default behavior

3. **Verify MightCounterfactual Definition**
   - Check if `MightCounterfactualOperator` definition matches default
   - Ensure derived definition produces equivalent semantics

### Phase 3: Testing and Validation (Medium Priority)

1. **Run Comparative Tests**
   ```bash
   # Test both theories with same examples
   ./dev_cli.py /src/model_checker/theory_lib/default/examples/counterfactual.py > default_results.txt
   ./dev_cli.py /src/model_checker/theory_lib/logos/subtheories/counterfactual/examples.py > logos_results.txt
   
   # Compare results systematically
   diff default_results.txt logos_results.txt
   ```

2. **Create Regression Tests**
   - Add tests ensuring logos and default theories give same results
   - Focus on problematic cases like CF_CM_2
   - Include both countermodel and theorem examples

3. **Validate All Counterfactual Examples**
   - Ensure all CF_CM_* examples produce expected countermodels
   - Ensure all CF_TH_* examples produce expected validations
   - Document any remaining discrepancies

### Phase 4: Documentation and Cleanup (Low Priority)

1. **Update Theory Documentation**
   - Document alignment between default and logos theories
   - Explain any intentional semantic differences
   - Update README files if needed

2. **Code Quality Improvements**
   - Remove placeholder implementations
   - Add comprehensive docstrings
   - Ensure consistent code style

## Files Requiring Attention

### Immediate (Phase 1-2)
- `/src/model_checker/theory_lib/default/operators.py` (analysis)
- `/src/model_checker/theory_lib/logos/subtheories/counterfactual/operators.py` (modification)
- `/src/model_checker/theory_lib/logos/semantic.py` (modification)

### Secondary (Phase 3)
- `/src/model_checker/theory_lib/default/examples/counterfactual.py` (reference)
- `/src/model_checker/theory_lib/logos/subtheories/counterfactual/examples.py` (testing)

### Documentation (Phase 4)
- `/src/model_checker/theory_lib/logos/README.md`
- `/src/model_checker/theory_lib/logos/subtheories/counterfactual/README.md`

## Success Criteria

1. **Semantic Equivalence**: Logos and default theories produce identical results for all counterfactual examples
2. **Test Validation**: All CF_CM_* examples find expected countermodels in both theories
3. **Theorem Verification**: All CF_TH_* examples validate as theorems in both theories  
4. **No Regressions**: Other logos subtheories (extensional, modal, etc.) continue working correctly

## Risk Assessment

- **High Risk**: Changes to core semantic methods may affect other operators
- **Medium Risk**: World closeness implementation may be complex
- **Low Risk**: Example alignment already completed successfully

## Estimated Effort

- **Phase 1**: 2-3 hours (analysis and comparison)
- **Phase 2**: 4-6 hours (implementation alignment)  
- **Phase 3**: 2-3 hours (testing and validation)
- **Phase 4**: 1-2 hours (documentation)

**Total**: 9-14 hours of focused development work