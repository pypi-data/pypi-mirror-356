use crate::{matrix::{DiagonalMatrix, Matrix}, Float};

pub fn diagonal_distance<M: Matrix>(
    a: &[Float],
    b: &[Float],
    init_val: Float,
    sakoe_chiba_band: Float,
    init_lambda: impl Fn(&[Float], &[Float], usize, usize, Float, Float, Float) -> Float + Copy,
    dist_lambda: impl Fn(&[Float], &[Float], usize, usize, Float, Float, Float) -> Float + Copy,
) -> Float {
    diagonal_distance_::<M>(
        a.len(),
        b.len(),
        init_val,
        sakoe_chiba_band,
        |i, j, x, y, z| init_lambda(&a, &b, i, j, x, y, z),
        |i, j, x, y, z| dist_lambda(&a, &b, i, j, x, y, z),
    )
}

fn diagonal_distance_<M: Matrix>(
    a_len: usize,
    b_len: usize,
    init_val: Float,
    sakoe_chiba_band: Float,
    init_lambda: impl Fn(usize, usize, Float, Float, Float) -> Float,
    dist_lambda: impl Fn(usize, usize, Float, Float, Float) -> Float,
) -> Float {
    let mut matrix = DiagonalMatrix::new(a_len, b_len, init_val);

    let mut i = 0;
    let mut j = 0;
    let mut s = 0;
    let mut e = 0;

    matrix.set_diagonal_cell(0, 0, 0.0);

    let start_coord = M::index_mat_to_diag(0, 0).1;
    let end_coord = M::index_mat_to_diag(a_len, b_len).1;

    let band_size = sakoe_chiba_band * (a_len as Float);

    for d in 2..(a_len + b_len + 1) {
        matrix.set_diagonal_cell(d, d as isize, init_val);

        let (s_, e_) = if sakoe_chiba_band < 1.0 {
            let mid_coord = start_coord as Float
                + (end_coord as Float - start_coord as Float) / (a_len + b_len) as Float * d as Float;
            (
                s.max((mid_coord - band_size).floor() as isize),
                e.min((mid_coord + band_size).ceil() as isize),
            )
        } else {
            (s, e)
        };

        let mut i1: usize = i;
        let mut j1: usize = j;

        let mut s_step = s;

        // Pre init for sakoe chiba band skipped cells
        for k in (s..s_).step_by(2) {
            matrix.set_diagonal_cell(d, k, init_val);
            i1 = i1.wrapping_sub(1);
            j1 += 1;
            s_step += 2;
        }

        for k in (s_step..e_ + 1).step_by(2) {
            let dleft = matrix.get_diagonal_cell(d - 1, k - 1);
            let ddiag = matrix.get_diagonal_cell(d - 2, k);
            let dup = matrix.get_diagonal_cell(d - 1, k + 1);

            matrix.set_diagonal_cell(
                d,
                k,
                if i1 == 1 || j1 == 1 {
                    init_lambda(i1, j1, dleft, ddiag, dup)
                } else {
                    dist_lambda(i1, j1, dleft, ddiag, dup)
                },
            );
            i1 = i1.wrapping_sub(1);
            j1 += 1;
            s_step += 2;
        }

        // Post init for sakoe chiba band skipped cells
        for k in (s_step..(e + 1)).step_by(2) {
            matrix.set_diagonal_cell(d, k, init_val);
            i1 = i1.wrapping_sub(1);
            j1 += 1;
        }

        if d <= a_len {
            i += 1;
            s -= 1;
            e += 1;
        } else if d <= b_len {
            j += 1;
            s += 1;
            e += 1;
        } else {
            j += 1;
            s += 1;
            e -= 1;
        }
    }

    let (rx, cx) = M::index_mat_to_diag(a_len, b_len);
    matrix.get_diagonal_cell(rx, cx)
}
