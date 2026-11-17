import { GROWTH, growthOf } from "./cost";

/** "What do O(n) and O(1) mean?": the same short explainer on every lesson, for newcomers. */
export function CostHelp({ time, space }: { time: string; space: string }) {
  const timeRow = growthOf(time)?.o;
  const spaceRow = growthOf(space)?.o;
  return (
    <details className="more cost-help">
      <summary>New to this? What O(n) and O(1) mean</summary>
      <div className="cost-help-body">
        <p>
          These labels (called <strong>Big-O</strong>) say how the work grows as the input grows.{" "}
          <code>n</code> is the size of the input, such as how many numbers are in the list. Small fixed
          costs are left out; only the part that matters for big inputs is kept.
        </p>
        <table className="growth">
          <thead>
            <tr>
              <th scope="col">Cost</th>
              <th scope="col">Steps when n = 1,000</th>
              <th scope="col">Grows like this when…</th>
            </tr>
          </thead>
          <tbody>
            {GROWTH.map((g) => {
              const notes = [g.o === timeRow && "this time", g.o === spaceRow && "this space"].filter(Boolean);
              return (
                <tr key={g.o} className={notes.length ? "growth-here" : undefined}>
                  <th scope="row">
                    <code>{g.o}</code>
                    {notes.length > 0 && <span className="growth-tag">{notes.join(" · ")}</span>}
                  </th>
                  <td>{g.steps}</td>
                  <td>{g.says}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <p>
          With two sizes, both appear: for a grid of <code>m</code> rows and <code>n</code> columns,{" "}
          <code>O(m · n)</code> means about one step per cell. <strong>Extra space</strong> is the memory
          the solution needs on top of its input; <code>O(1)</code> there means just a few variables,
          however big the input is.
        </p>
      </div>
    </details>
  );
}
